# Plow hosted variant

This variant addresses the organizer's [September 24 reply](https://discord.com/channels/1519035948191449268/1544106357865586718/1552884751155863612): Plow messaging, automatic per-install reporting, and host-supported credentials.

It inherits the official [Plow OpenClaw base](https://github.com/plow-pbc/plow-openclaw-agent/tree/7ce757a1745de286dd180c5c5182aca31eba8a75), pinned to published digest `sha256:6e5e1a11a8c6e2ef6ecaa5e7b429e778a9a3befaf416a09922aaaa4a5b21d647`. The runtime is OpenClaw 2026.9.4. Do not attach the native 2026.9.5 state volume: that would be an unsupported database downgrade.

The inherited channel handles Plow owner chats and group conversations. The recruiter prompt permits a shared evidence review only after the actual owner authorizes that trusted room, its collaborators, and its scope. Shared files and tools are not privacy isolation. Hiring decisions remain human; sending to other conversations is disabled in the variant config.

The official reporter registers each installation using its Plow credential, persists its own Index key and ledger under `/var/lib/plow`, refreshes the collector, and reports every five minutes. Never bake the developer's Index key, account token, NVIDIA key, or runtime state into the image. Preserve the hosted volume across restarts; each separate installation needs its own volume. `AGENT_ID=recruiter-associate` enables this inherited reporter. Offline checks override it to empty and disable networking. No simulated usage should be reported.

## Approved hosted model

The published base offers Plow's `z-ai/glm-5.2` route with a Claude fallback. This variant removes the fallback and requires an explicit `RECRUITER_CLOUD_MODEL=z-ai/glm-5.2` setting. The project owner explicitly approved this route on September 25, 2026. The cloud image sets it at build time, requiring no NVIDIA key or manual model setup. Offline config and gateway checks do not make a model request. NVIDIA GLM 5.3 remains the native installer route.

The publication workflow produces a distinct `cloud` tag and immutable digest. The organizers must verify a fresh hosted reply and usage attributed to separate installs. A passing offline probe does not establish either live behavior.

## Build and verify

```sh
docker build -f deploy/cloud/Dockerfile -t recruiter-cloud:check .
docker run --rm --network none --entrypoint node recruiter-cloud:check /opt/recruiter/cloud-check.mjs
docker run --rm --network none -e AGENT_ID= -e RECRUITER_CLOUD_MODEL=z-ai/glm-5.2 recruiter-cloud:check /opt/plow/probe
```

The manual `Publish recruiter cloud container` GitHub workflow runs these checks without placing the base image on the developer's Mac. After checks pass it publishes the cloud image to GHCR. It does not deploy, send messages, or submit usage.

Our added code and prompt are MIT licensed. The upstream repository does not publish a root source license; we inherit its documented public base image and do not copy its source into this repository. Its components retain their own terms.

Verified September 25: [GitHub run36174574457](https://github.com/scking21/recruiter-associate/actions/runs/36174574457) passed image build, config/reporting contract checks, recruiter CLI loading, and actual OpenClaw gateway/Plow plugin startup in 1m41s. Networking and Index reporting were disabled. No hosted model reply or accepted report is claimed. The pinned published base predates the upstream dashboard and email drain updates; the recruiter workflow does not enable cross-conversation sends.
