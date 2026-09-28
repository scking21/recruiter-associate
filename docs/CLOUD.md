# Plow hosted variant

## Registry outage recovery

Run `36467808939` passed the new source tests but could not fetch the original pinned ECR manifest: HTTP 429, data limit exceeded. The workflow now offers `reuse_verified_release`, default false. Setting it true builds from the exact earlier verified Roletrace image `sha256:ad99da3f5bf6643f52df1a614036ce17c98c2547cd1645dc15f3ed2c4839fde4` on GHCR. The choice is hardcoded, not an arbitrary image input. That parent preserves the same upstream runtime and approved model; it is not a provider fallback.

The Dockerfile preserves an existing original `config-upstream.js` so it never wraps the Roletrace wrapper recursively. All source copies, offline config checks, packaged presentation tests and network-disabled gateway/plugin probe still run. This source delta adds or changes copied files and removes none; before reusing the recovery path for a future delta, check for deleted overlay files that would otherwise persist in the parent. Upstream assurance comes from the prior verified build rather than a fresh ECR pull. Promotion to the Index remains a separate step after a successful build.

Recovery release verified September 28 at 18:55 UTC: [run36468209995](https://github.com/scking21/roletrace/actions/runs/36468209995), source `a7ef7b7`, passed all steps including 26 recruiter source tests, 14 packaged presentation tests and actual offline gateway/plugin startup. Published and promoted image: `ghcr.io/scking21/recruiter-associate@sha256:8f420308e79462dc189de798b11129396d901933dd60ec3f95fc34acfdebc0dc`. Anonymous manifest/config inspection proved its layer list begins with the complete verified parent layer list, retained the parent user/entrypoint/command and kept `AGENT_NAME=Roletrace`, `AGENT_ID=recruiter-associate`, and `RECRUITER_CLOUD_MODEL=z-ai/glm-5.2`. Official CLI promotion and a separate public read confirmed the enabled new-install pin. Metadata readback preserved the existing video and verification/deployability, with the revised correction-focused blurb. No hosted inference or usage report was invoked by this verification.

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

The manual `Publish Roletrace cloud container` GitHub workflow runs these checks without placing the base image on the developer's Mac. After checks pass it publishes the cloud image to GHCR. It does not deploy, send messages, or submit usage.

Our added code and prompt are MIT licensed. The upstream repository does not publish a root source license; we inherit its documented public base image and do not copy its source into this repository. Its components retain their own terms.

Verified September 25: [GitHub run36174574457](https://github.com/scking21/roletrace/actions/runs/36174574457) passed image build, config/reporting contract checks, recruiter CLI loading, and actual OpenClaw gateway/Plow plugin startup in 1m41s. Networking and Index reporting were disabled. No hosted model reply or accepted report is claimed. The pinned published base predates the upstream dashboard and email drain updates; the recruiter workflow does not enable cross-conversation sends.

Published September 25: `ghcr.io/scking21/recruiter-associate@sha256:d66103775763b06c969bab68ee175bffec20e6ffa390b54186c6520cc7fdd3a6`. [Publication and checks](https://github.com/scking21/roletrace/actions/runs/36175691282) passed in 3m17s. Anonymous GHCR manifest/config access verified the baked-in model, AGENT_ID, persistent state path, and inherited boot command. No NVIDIA or Plow bearer is baked into the image. Digest sent as a reply to the organizer request; fresh hosted response, accepted per-install usage and one-click admission remain pending.

[Organizer follow-up with published cloud digest](https://discord.com/channels/1519035948191449268/1544106357865586718/1553117041001496658).

## September 28 intake update

Source commit `63545e2` simplifies conversational intake and assigns neutral internal IDs without weakening explicit authorization or source assertions. [Build 36422188892](https://github.com/scking21/roletrace/actions/runs/36422188892) passed offline configuration and actual gateway/plugin startup checks. Published image: `ghcr.io/scking21/recruiter-associate@sha256:5fb6c312f188b043cbf4493927d1b2b3515e480bce45f119dfbabd27dcb42910`. Plow promotion succeeded and the enabled pin was read back at 2026-09-28T12:32:55+00:00. This supersedes the earlier digest for new installs only. Existing agents are unchanged. Fresh hosted inference and real-user review are not established by these offline checks.

## Roletrace release, September 28

Source `f85cd72` applies the Roletrace display name without changing agent identity or the approved provider. [Build 36424027061](https://github.com/scking21/roletrace/actions/runs/36424027061) passed config/reporting checks and actual offline gateway/plugin startup. Anonymous registry access verified `AGENT_NAME=Roletrace`, retained `AGENT_ID=recruiter-associate`, and `RECRUITER_CLOUD_MODEL=z-ai/glm-5.2`. The enabled new-install pin was promoted and read back as `ghcr.io/scking21/recruiter-associate@sha256:ad99da3f5bf6643f52df1a614036ce17c98c2547cd1645dc15f3ed2c4839fde4` on September 28 at 12:49 UTC. Existing hosted installations remain unchanged. The internal Plow catalog label still says Recruiter associate; the public Index name is Roletrace. The official owner CLI exposes Index display updates but no separate catalog-name migration.
