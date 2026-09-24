# Native OpenClaw installation

Requirements: Python 3.10+, installed OpenClaw, and your own authorized NVIDIA credential. The installer was adapted from the verified Trail runtime fixes; this recruiter deployment must be checked separately before claiming live readiness.

```sh
git clone https://github.com/scking21/recruiter-associate.git
cd recruiter-associate
python3 scripts/recruiter_agent.py prepare
# Supply NVIDIA_API_KEY from your credential manager; never commit it.
python3 scripts/recruiter_agent.py start
```

The gateway runs in the foreground on loopback port 20789. State lives under `runtime/openclaw-state`; the existing default gateway and parked Trail runtime are not modified. Keep the terminal running. No public transport, automatic startup or cloud deployment is configured.

In another shell with the same credential environment:

```sh
python3 scripts/recruiter_agent.py status
python3 scripts/recruiter_agent.py dashboard
python3 scripts/recruiter_agent.py chat --message "Read the recruiter-associate skill and explain the required inputs. Do not run a benchmark or contact anyone."
```

The workspace is `runtime/openclaw-state/workspace`. Put authorized inputs under `inputs/`, keep results under `work/`, and use the installed `./recruiter-tool` launcher. It pins the Python used during preparation to avoid the macOS Python 3.9 mismatch. Prepare refuses existing state; preserve the directory and restart it rather than making a fresh installation identity.

Only NVIDIA `z-ai/glm-5.3` is configured, with no model fallback. Streaming usage metadata is enabled. Scheduled heartbeats are disabled. Credentials are supplied through environment references and a private gateway token. Check your current provider entitlement before live use; no paid hosting is provisioned.

This is an owner environment, not a hostile participant sandbox. Workspace file restrictions do not sandbox shell execution. Never publish its administrator URL or token. Complete the separate multiplayer and organizer gates in [HACKATHON.md](HACKATHON.md).


## Repository extraction checks, September 24

Fresh isolated configuration passed `openclaw config validate` on OpenClaw 2026.9.5. The installed pinned `recruiter-tool --help` command also passed. These checks did not launch a gateway or make a model request. The default macOS Python 3.9 was correctly rejected; this Mac used `/Users/corby/homebrew/bin/python3` (Python 3.14) to prepare the package. Use an interpreter of at least 3.10 on your machine.
