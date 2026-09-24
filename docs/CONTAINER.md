# Docker installation

Use Docker to package the same native recruiter agent for another machine. This does not enable Agent Index registration, Plow connectors or multiplayer by itself.

## Build and run

Supply your authorized `NVIDIA_API_KEY` through your shell or credential manager. Do not paste it into tracked files. Then run:

```sh
docker compose up --build -d
docker compose exec recruiter python3 scripts/container_entrypoint.py health
```

The service runs as an unprivileged user. It listens inside the container on 20789 and is published only at `127.0.0.1:20790` on this computer. Port 20789 remains available to the separate native installation. No host folders or Docker socket are mounted. `.dockerignore` admits only specified source files; runtime, credentials, local reviews and Git history are excluded.

The named volume `recruiter-state` retains config, workspace, conversations and install identity. `docker compose stop` stops this project. Preserve the volume when updating; deleting it loses the installation identity and work. Automatic restart is disabled.

## Browser pairing

The browser still needs OpenClaw authentication. In your own private terminal, ask OpenClaw for its owner pairing link:

```sh
docker compose exec recruiter sh -c 'export OPENCLAW_CONFIG_PATH=/data/recruiter/openclaw.json; export RECRUITER_OPENCLAW_GATEWAY_TOKEN="$(cat /data/recruiter/gateway-token)"; openclaw dashboard --no-open'
```

Keep the resulting pairing link private. When opening it on this computer, change only the port from 20789 to the published host port 20790, leaving the rest of the link intact. Never share an owner pairing link with applicants. Public deployment requires separate transport and participant identity configuration; do not widen the host port binding just to get a demo link.

## Verification

On September 24, a local Linux arm64 image built successfully with OpenClaw 2026.9.5, Node 24.16.0 and Python 3.11. Fresh startup and authenticated gateway health passed. After restart, health passed again and the private gateway identity fingerprint was unchanged. No provider request ran inside the container.

The manually dispatched repository workflow builds Linux amd64, checks gateway startup using a dummy credential without model requests, and publishes the image with a repository scoped GitHub token. Package visibility and anonymous pull must be verified separately before claiming a public ready to install image. This package is not the Plow base image and does not claim organizer one click compatibility.
