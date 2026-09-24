"""Container adapter: preserve one private install identity across restarts."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from recruiter_agent import InstallError, ensure_openclaw, paths, prepare, runtime_env


def main() -> int:
    os.umask(0o077)
    root = Path(os.environ.get("RECRUITER_STATE_ROOT", "/data/recruiter"))
    health = len(sys.argv) == 2 and sys.argv[1] == "health"
    if len(sys.argv) > 1 and not health:
        raise InstallError("only the optional health command is supported")
    if not root.exists():
        if health:
            raise InstallError("container install is not ready")
        if not os.environ.get("NVIDIA_API_KEY"):
            raise InstallError("NVIDIA_API_KEY is required")
        prepare(root, 20789, False)
        config_path = paths(root)["config"]
        config = json.loads(config_path.read_text())
        # Docker publishes this listener only on the host's loopback interface.
        config["gateway"]["bind"] = "lan"
        config["gateway"]["controlUi"]["allowedOrigins"] = [
            "http://127.0.0.1:20790", "http://localhost:20790"
        ]
        config_path.write_text(json.dumps(config, indent=2) + "\n")
    env = runtime_env(paths(root), require_nvidia=not health)
    executable = ensure_openclaw()
    arguments = [executable, "gateway", "health"] if health else [
        executable, "gateway", "run", "--bind", "lan", "--port", "20789"
    ]
    os.execvpe(executable, arguments, env)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InstallError, OSError, ValueError) as error:
        print(f"recruiter container: {error}", file=sys.stderr)
        raise SystemExit(2)
