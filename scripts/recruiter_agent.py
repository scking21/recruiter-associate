#!/usr/bin/env python3
"""Prepare and operate an isolated native OpenClaw Recruiter associate agent."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import shutil
import stat
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "runtime" / "openclaw-state"
DEFAULT_PORT = 20789
AGENT_ID = "recruiter-associate"
MODEL_REF = "nvidia/z-ai/glm-5.3"


class InstallError(RuntimeError):
    """Raised when an isolated install cannot be prepared safely."""


def paths(root: Path) -> dict[str, Path]:
    resolved = root.expanduser().resolve()
    return {
        "root": resolved,
        "config": resolved / "openclaw.json",
        "token": resolved / "gateway-token",
        "workspace": resolved / "workspace",
    }


def config_for(targets: dict[str, Path], port: int) -> dict[str, object]:
    workspace = str(targets["workspace"])
    return {
        "secrets": {
            "providers": {
                "recruiter_env": {
                    "source": "env",
                    "allowlist": ["NVIDIA_API_KEY", "RECRUITER_OPENCLAW_GATEWAY_TOKEN"],
                }
            }
        },
        "models": {
            "mode": "replace",
            "providers": {
                "nvidia": {
                    "baseUrl": "https://integrate.api.nvidia.com/v1",
                    "apiKey": {
                        "source": "env",
                        "provider": "recruiter_env",
                        "id": "NVIDIA_API_KEY",
                    },
                    "api": "openai-completions",
                    "models": [
                        {
                            "id": "z-ai/glm-5.3",
                            "name": "GLM 5.3",
                            "reasoning": True,
                            "input": ["text"],
                            "maxTokens": 4096,
                            "compat": {"supportsUsageInStreaming": True},
                            "params": {
                                "chat_template_kwargs": {"clear_thinking": True},
                                "extra_body": {"reasoning_effort": "low"},
                            },
                        }
                    ],
                }
            },
        },
        "agents": {
            "defaults": {
                "utilityModel": "",
                "workspace": workspace,
                "timeoutSeconds": 180,
                "bootstrapMaxChars": 12000,
                "bootstrapTotalMaxChars": 16000,
                "heartbeat": {"every": "0m"},
            },
            "entries": {
                AGENT_ID: {
                    "name": "Recruiter associate",
                    "description": "Prepare job-related evidence review drafts for human hiring review.",
                    "workspace": workspace,
                    "model": {"primary": MODEL_REF, "fallbacks": []},
                    "modelPolicy": {"allow": [MODEL_REF]},
                    "thinkingDefault": "off",
                    "skills": ["recruiter-associate"],
                    "subagents": {"allowAgents": []},
                    "tools": {
                        "allow": ["read", "write", "edit", "exec", "process"],
                        "deny": [
                            "message",
                            "sessions_spawn",
                            "sessions_send",
                            "gateway",
                            "browser",
                            "web_search",
                            "web_fetch",
                        ],
                        "exec": {
                            "host": "gateway",
                            "security": "full",
                            "ask": "off",
                            "strictInlineEval": True,
                            "notifyOnExit": False,
                        },
                        "fs": {"workspaceOnly": True},
                        "message": {
                            "crossContext": {
                                "allowWithinProvider": False,
                                "allowAcrossProviders": False,
                            },
                            "actions": {"allow": []},
                            "broadcast": {"enabled": False},
                        },
                    },
                }
            },
        },
        "tools": {"fs": {"workspaceOnly": True}},
        "gateway": {
            "mode": "local",
            "port": port,
            "bind": "loopback",
            "auth": {
                "mode": "token",
                "token": {
                    "source": "env",
                    "provider": "recruiter_env",
                    "id": "RECRUITER_OPENCLAW_GATEWAY_TOKEN",
                },
            },
            "controlUi": {
                "sessionObserver": False,
                "automaticallyFetchFavicons": False,
                "communityInvite": False,
            },
            "cliAgents": {"enabled": False},
            "terminal": {"enabled": False},
        },
    }


def ensure_openclaw() -> str:
    executable = shutil.which("openclaw")
    if executable is None:
        raise InstallError("openclaw is not on PATH; install it before using this helper")
    node = shutil.which("node")
    if not node:
        raise InstallError("Node.js is missing from PATH; use Node 24.16+ (24.x) or 26.1+")
    try:
        result = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=10, check=True)
        version = tuple(int(part) for part in result.stdout.strip().removeprefix("v").split("."))
    except (ValueError, subprocess.SubprocessError) as error:
        raise InstallError("cannot determine Node.js version; activate a supported Node runtime") from error
    if len(version) != 3 or not ((24, 16, 0) <= version < (25, 0, 0) or version >= (26, 1, 0)):
        raise InstallError(f"Node {result.stdout.strip()} on PATH is unsupported by OpenClaw 2026.9.5; activate Node 24.16+ (24.x) or 26.1+")
    return executable


def recruiter_python() -> Path:
    if sys.version_info < (3, 10):
        raise InstallError(
            "prepare requires Python 3.10 or newer because the recruiter workflow uses zip(strict=True)"
        )
    executable = Path(sys.executable).resolve()
    if not executable.is_file():
        raise InstallError(f"could not resolve the prepare Python executable: {executable}")
    if any(character.isspace() for character in str(executable)):
        raise InstallError(f"Python executable path cannot contain whitespace: {executable}")
    return executable


def install_recruiter_launcher(workspace: Path, python: Path) -> None:
    launcher = workspace / "recruiter-tool"
    launcher.write_text(
        f"#!{python}\n"
        "from recruiter.cli import main\n"
        "raise SystemExit(main())\n",
        encoding="utf-8",
    )
    launcher.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    skill_path = workspace / "skills" / "recruiter-associate" / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    old_command = "python3 -m recruiter"
    if old_command not in skill_text and "./recruiter-tool" not in skill_text:
        raise InstallError(f"copied skill does not contain its expected workflow command: {skill_path}")
    skill_path.write_text(skill_text.replace(old_command, "./recruiter-tool"), encoding="utf-8")


def prepare(root: Path, port: int, dry_run: bool) -> None:
    targets = paths(root)
    python = recruiter_python()
    if targets["root"].exists():
        raise InstallError(f"refusing to overwrite existing state root: {targets['root']}")

    if dry_run:
        print(f"would prepare isolated OpenClaw state: {targets['root']}")
        print(f"would create workspace: {targets['workspace']}")
        print(f"would configure agent {AGENT_ID} on loopback port {port}")
        return

    ensure_openclaw()
    targets["root"].mkdir(parents=True, exist_ok=True)
    targets["workspace"].mkdir(mode=0o700)
    try:
        shutil.copytree(
            REPO_ROOT / "recruiter",
            targets["workspace"] / "recruiter",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        shutil.copytree(REPO_ROOT / "experiments", targets["workspace"] / "experiments", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        skill_dir = targets["workspace"] / "skills" / "recruiter-associate"
        skill_dir.parent.mkdir()
        shutil.copytree(REPO_ROOT / "skills" / "recruiter-associate", skill_dir)
        shutil.copy2(REPO_ROOT / "deploy" / "AGENTS.md", targets["workspace"] / "AGENTS.md")
        (targets["workspace"] / "docs").mkdir()
        shutil.copy2(REPO_ROOT / "docs" / "WORKFLOW.md", targets["workspace"] / "docs" / "WORKFLOW.md")
        install_recruiter_launcher(targets["workspace"], python)
        (targets["workspace"] / "inputs").mkdir()
        (targets["workspace"] / "work").mkdir()

        token_fd = os.open(
            targets["token"],
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            stat.S_IRUSR | stat.S_IWUSR,
        )
        with os.fdopen(token_fd, "w", encoding="utf-8") as token_file:
            token_file.write(secrets.token_urlsafe(48) + "\n")
        with targets["config"].open("x", encoding="utf-8") as output:
            json.dump(config_for(targets, port), output, indent=2, sort_keys=True)
            output.write("\n")
        targets["config"].chmod(stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        # The target did not exist before this call, so this rollback cannot erase an older install.
        shutil.rmtree(targets["root"], ignore_errors=True)
        raise

    print(f"prepared isolated OpenClaw state: {targets['root']}")
    print(f"workspace ready: {targets['workspace']}")
    print("set NVIDIA_API_KEY in the shell before start or chat")


def runtime_env(targets: dict[str, Path], *, require_nvidia: bool) -> dict[str, str]:
    if not targets["config"].is_file() or not targets["workspace"].is_dir():
        raise InstallError("install is not prepared; run prepare first")
    if not targets["token"].is_file():
        raise InstallError(f"gateway token is missing: {targets['token']}")
    token_mode = stat.S_IMODE(targets["token"].stat().st_mode)
    if token_mode != 0o600:
        raise InstallError(f"gateway token must have mode 600, found {token_mode:o}")
    if require_nvidia and not os.environ.get("NVIDIA_API_KEY"):
        raise InstallError("NVIDIA_API_KEY is not set")
    env = os.environ.copy()
    env["OPENCLAW_STATE_DIR"] = str(targets["root"])
    env["OPENCLAW_CONFIG_PATH"] = str(targets["config"])
    env["RECRUITER_OPENCLAW_GATEWAY_TOKEN"] = targets["token"].read_text(encoding="utf-8").strip()
    return env


def run_openclaw(
    root: Path,
    arguments: list[str],
    *,
    require_nvidia: bool = False,
    capture: bool = False,
) -> int:
    targets = paths(root)
    env = runtime_env(targets, require_nvidia=require_nvidia)
    command = [ensure_openclaw(), *arguments]
    if capture:
        result = subprocess.run(command, env=env, text=True, capture_output=True, check=False)
        if result.returncode:
            if result.stderr:
                sys.stderr.write(result.stderr)
            raise InstallError(f"openclaw command failed with exit code {result.returncode}")
        return result.returncode
    return subprocess.run(command, env=env, check=False).returncode


def show_status(root: Path) -> int:
    targets = paths(root)
    print(f"state: {targets['root']}")
    print(f"config: {'ready' if targets['config'].is_file() else 'missing'}")
    print(f"workspace: {'ready' if targets['workspace'].is_dir() else 'missing'}")
    print(f"gateway token: {'ready' if targets['token'].is_file() else 'missing'}")
    if not all((targets["config"].is_file(), targets["workspace"].is_dir(), targets["token"].is_file())):
        return 1
    validation = run_openclaw(root, ["config", "validate"])
    if validation:
        return validation
    return run_openclaw(root, ["gateway", "health"])


def configured_port(root: Path) -> int:
    config_path = paths(root)["config"]
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        port = data["gateway"]["port"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        raise InstallError(f"could not read gateway port from {config_path}: {error}") from error
    if type(port) is not int or not 1 <= port <= 65535:
        raise InstallError(f"invalid gateway port in {config_path}")
    return port


def open_dashboard(root: Path, *, no_open: bool) -> int:
    targets = paths(root)
    env = runtime_env(targets, require_nvidia=False)
    result = subprocess.run(
        [ensure_openclaw(), "dashboard", "--no-open", "--json"],
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        if result.stderr:
            sys.stderr.write(result.stderr)
        raise InstallError(f"openclaw dashboard failed with exit code {result.returncode}")
    try:
        details = json.loads(result.stdout)
        browser_url = details["browserUrl"]
        public_url = details["httpUrl"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise InstallError("openclaw dashboard returned an invalid browserUrl") from error
    parsed = urlparse(browser_url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise InstallError("openclaw dashboard returned a non-loopback URL")
    public_parsed = urlparse(public_url)
    if (
        public_parsed.scheme not in {"http", "https"}
        or public_parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or public_parsed.query
        or public_parsed.fragment
    ):
        raise InstallError("openclaw dashboard returned an invalid public URL")
    if no_open:
        print(f"dashboard base URL: {public_url}")
        print("the tokenized pairing URL was suppressed; rerun without --no-open to open it privately")
        return 0
    if not webbrowser.open(browser_url):
        raise InstallError("could not open the dashboard in a browser")
    print(f"opened dashboard at {public_url}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="isolated OpenClaw state root")
    commands = parser.add_subparsers(dest="command", required=True)

    prepare_parser = commands.add_parser("prepare", help="create the isolated config and workspace")
    prepare_parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    prepare_parser.add_argument("--dry-run", action="store_true")

    commands.add_parser("status", help="validate config and check gateway health")
    start_parser = commands.add_parser("start", help="run the isolated gateway in the foreground")
    start_parser.add_argument("--port", type=int, help="temporary port override")

    chat_parser = commands.add_parser("chat", help="send one owner message to the dedicated agent")
    message = chat_parser.add_mutually_exclusive_group(required=True)
    message.add_argument("--message")
    message.add_argument("--message-file", type=Path)

    dashboard_parser = commands.add_parser("dashboard", help="open the native dashboard without printing its token")
    dashboard_parser.add_argument("--no-open", action="store_true", help="show only the unpaired loopback base URL")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "prepare":
            if not 1 <= args.port <= 65535:
                raise InstallError("port must be between 1 and 65535")
            prepare(args.root, args.port, args.dry_run)
            return 0
        if args.command == "status":
            return show_status(args.root)
        if args.command == "start":
            port = args.port if args.port is not None else configured_port(args.root)
            if not 1 <= port <= 65535:
                raise InstallError("port must be between 1 and 65535")
            return run_openclaw(
                args.root,
                ["gateway", "run", "--port", str(port), "--bind", "loopback"],
                require_nvidia=True,
            )
        if args.command == "chat":
            command = ["agent", "--agent", AGENT_ID, "--thinking", "off"]
            if args.message is not None:
                command.extend(["--message", args.message])
            else:
                command.extend(["--message-file", str(args.message_file.resolve())])
            return run_openclaw(args.root, command, require_nvidia=True)
        if args.command == "dashboard":
            return open_dashboard(args.root, no_open=args.no_open)
    except (InstallError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
