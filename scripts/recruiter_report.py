#!/usr/bin/env python3
"""Preview or explicitly publish Recruiter associate OpenClaw usage.

The default command is read only.  It reads the one allowed OpenClaw agent
store through the vendored Agent Index collector and prints aggregate counts.
Use ``--report`` only after the install has an Agent Index report key.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


AGENT_ID = "recruiter-associate"
ALLOWED_MODELS = frozenset({"z-ai/glm-5.3", "nvidia/z-ai/glm-5.3"})
PUBLIC_NAME = "Recruiter associate"
PUBLIC_BLURB = (
    "Prepares cited job-related evidence reviews for a human hiring owner; "
    "external multiplayer and real applicant usage remain unverified."
)
PUBLIC_REPO = "https://github.com/scking21/recruiter-associate"
PUBLIC_INSTALL_URL = f"{PUBLIC_REPO}/blob/main/docs/INSTALL.md"
PUBLIC_RUNTIME = "Python 3.10+ standard library; OpenClaw 2.0"
CLIENT_PATH = (
    Path(__file__).resolve().parents[1]
    / "vendor"
    / "agent-index-client"
    / "agent_index_client.py"
)


class ReportingError(Exception):
    """A fail closed local reporting error."""


def _load_client() -> Any:
    """Load the vendored client without importing a package from the host."""
    if not CLIENT_PATH.is_file():
        raise ReportingError(f"vendored client is missing: {CLIENT_PATH}")
    spec = importlib.util.spec_from_file_location("recruiter_vendored_agent_index", CLIENT_PATH)
    if spec is None or spec.loader is None:
        raise ReportingError("could not load the vendored Agent Index client")
    client = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(client)
    return client


def _validate_state_dir(value: Path) -> tuple[Path, Path]:
    """Require exactly one OpenClaw store for the fixed entry agent."""
    root = value.expanduser().resolve()
    agents = root / "agents"
    if not agents.is_dir():
        raise ReportingError("state directory has no agents directory")

    agent_paths = sorted(path for path in agents.iterdir() if path.is_dir())
    agent_dirs = [path.name for path in agent_paths]
    if agent_dirs != [AGENT_ID]:
        joined = ", ".join(agent_dirs) if agent_dirs else "none"
        raise ReportingError(
            f"state directory must contain only {AGENT_ID}; found {joined}"
        )

    agent_dir = agents / AGENT_ID
    if agent_dir.resolve() != agent_dir and not agent_dir.resolve().is_relative_to(root):
        raise ReportingError("agent directory resolves outside the state directory")
    store = agent_dir / "agent" / "openclaw-agent.sqlite"
    if not store.is_file():
        raise ReportingError(f"{AGENT_ID} OpenClaw store is missing")
    if not store.resolve().is_relative_to(root):
        raise ReportingError("OpenClaw store resolves outside the state directory")

    stores = sorted(agents.glob("*/agent/openclaw-agent.sqlite"))
    if stores != [store]:
        raise ReportingError("state directory does not have exactly one allowed store")
    return root, store


def _collect(client: Any, state_dir: Path, days: int) -> list[dict[str, Any]]:
    """Collect only OpenClaw usage and convert it to the official payload shape."""
    client.FAILURES.clear()
    usage = client.from_openclaw(days, str(state_dir))
    failures = tuple(client.FAILURES)
    if failures:
        # The vendored collector includes paths in some diagnostics.  Keep those
        # out of the command output, which is intended for a shared terminal.
        raise ReportingError(f"OpenClaw collection failed ({len(failures)} failure(s))")
    payload = client.merge(usage)
    models = {
        model.get("model")
        for day in payload
        for model in day.get("models", [])
        if isinstance(model, dict)
    }
    unexpected = sorted(model for model in models if model not in ALLOWED_MODELS)
    if unexpected:
        raise ReportingError("usage contains a model outside the approved route")
    return payload


def _json_payload(days: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the public, aggregate preview shape."""
    return {
        "agent": AGENT_ID,
        "transmitted": False,
        "days": days,
    }


@contextmanager
def _scoped_report_state(client: Any, state_dir: Path) -> Iterator[Path]:
    """Scope official client identity files to ``state_dir/reporting``."""
    reporting_dir = state_dir / "reporting"
    if reporting_dir.is_symlink():
        raise ReportingError("reporting state directory must not be a symlink")
    old_token_path = client.TOKEN_PATH
    old_state_path = client.STATE_PATH
    old_state_dir = client.state_dir
    try:
        # The official client resolves its report key through these globals and
        # state_dir(). Keep both inside the requested state directory without
        # changing HOME or touching the user's normal identity.
        client.TOKEN_PATH = str(reporting_dir / "token")
        client.STATE_PATH = str(reporting_dir / "hermes-state.json")
        client.state_dir = lambda: str(reporting_dir)
        yield reporting_dir
    finally:
        client.TOKEN_PATH = old_token_path
        client.STATE_PATH = old_state_path
        client.state_dir = old_state_dir


def _publish(client: Any, state_dir: Path, days: list[dict[str, Any]]) -> None:
    """Publish through the vendored client's own key and POST implementation."""
    if not days:
        raise ReportingError("no usage was collected; refusing to publish an empty report")
    with _scoped_report_state(client, state_dir):
        client.use_index()
        try:
            headers = client.auth_headers()
        except SystemExit as error:
            raise ReportingError("no scoped Agent Index report key is available") from error
        code, _body = client._post(
            f"{client.API}/v1/usage?agent_id={AGENT_ID}",
            {"days": days},
            headers,
        )
    if code != 200:
        raise ReportingError(f"Agent Index report was not accepted (status {code})")


def _register(client: Any, state_dir: Path, video_id: str | None) -> None:
    """Register fixed public metadata through the official client."""
    argv = [
        "--register",
        "--agent",
        AGENT_ID,
        "--name",
        PUBLIC_NAME,
        "--blurb",
        PUBLIC_BLURB,
        "--repo",
        PUBLIC_REPO,
        "--runtime",
        PUBLIC_RUNTIME,
        "--install-url",
        PUBLIC_INSTALL_URL,
    ]
    if video_id is not None:
        argv.extend(["--video", video_id])
    with _scoped_report_state(client, state_dir):
        client.use_index()
        try:
            result = client.register(AGENT_ID, argv)
        except SystemExit as error:
            raise ReportingError("Agent Index registration was refused") from error
    if result not in (None, 0):
        raise ReportingError(f"Agent Index registration failed (status {result})")


def _validate_video_id(value: str | None) -> str | None:
    if value is None:
        return None
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,64}", value):
        raise ReportingError("--video-id must be a YouTube video ID, not a URL")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--state-dir",
        type=Path,
        required=True,
        help="OpenClaw state root containing only agents/recruiter-associate",
    )
    parser.add_argument("--days", type=int, default=28, help="local day window (default: 28)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--report",
        action="store_true",
        help="publish through the official client; omitted means read-only preview",
    )
    mode.add_argument(
        "--register",
        action="store_true",
        help="register the fixed public page through the official client",
    )
    parser.add_argument(
        "--video-id",
        help="optional YouTube video ID for --register, never a URL",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.register and not os.environ.get("PLOW_AGENT_TOKEN"):
        print("recruiter report refused: --register requires PLOW_AGENT_TOKEN", file=sys.stderr)
        return 2
    if args.video_id is not None and not args.register:
        print("recruiter report refused: --video-id requires --register", file=sys.stderr)
        return 2
    if args.days <= 0 or args.days > 366:
        print("recruiter report refused: --days must be between 1 and 366", file=sys.stderr)
        return 2
    try:
        video_id = _validate_video_id(args.video_id)
        state_dir, _store = _validate_state_dir(args.state_dir)
        loaded = _load_client()
        if args.register:
            _register(loaded, state_dir, video_id)
            print(json.dumps({"agent": AGENT_ID, "registered": True}, sort_keys=True))
            return 0
        days = _collect(loaded, state_dir, args.days)
        if args.report:
            _publish(loaded, state_dir, days)
            print(json.dumps({"agent": AGENT_ID, "published": True}, sort_keys=True))
        else:
            print(json.dumps(_json_payload(days), indent=2, sort_keys=True))
        return 0
    except (OSError, ReportingError, TypeError, ValueError) as error:
        print(f"recruiter report refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
