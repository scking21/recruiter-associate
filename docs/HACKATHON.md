# OpenClaw Recruiter Hackathon Readiness

This is the selected recruiter route. It supersedes the old Trail priority. The prior recruiter experiment is useful synthetic evidence only; it does not establish a real hiring owner, applicant queue, deployment, multiplayer use, Agent Index reporting, or demand.

## Compliance matrix

| Requirement or gate | State | Evidence and next action |
| --- | --- | --- |
| Real startup hiring use case | **Blocked** | The product must own a real recruiting job for this startup. Identify the hiring owner and the job they authorize the agent to do. |
| OpenClaw 2.0 multiplayer | **Unverified** | The new repo has no confirmed OpenClaw 2.0 multiplayer run. The live flow must use an owner and an authorized collaborator who interact with the agent. Do not use fake applicants or invented collaborators. |
| Human hiring authority | **Implemented in prior experiment** | The old synthetic protocol kept every disposition with a human and excluded protected information. Recheck that boundary in the real workflow; synthetic results are not hiring validation. |
| Technical recruiter evidence | **Done in prior experiment** | The old repo records a refined guarded arm passing 7 of 7 synthetic gates. This is not evidence of real users, consent, adoption, or distribution. |
| Public Agent Index listing | **Blocked** | No listing, registration, public image, or confirmed deployment exists in this repo. The source is public; Agent Index registration remains separate. Here image means a deployable container, not the repository cover. |
| MIT license and official client reporting | **Source/license ready; reporting unverified** | MIT LICENSE is present and the public repository is created. The vendored official client retains Apache 2.0; actual usage submission and acceptance remain unverified. |
| Genuine usage and installs | **Blocked** | No confirmed real install or token usage exists. Use only genuine startup users and collaborators. Artificial usage, fabricated applicants, and self-generated leaderboard activity are prohibited. |
| Demo video, at least 60 seconds | **Deferred by user** | Stop before video creation or publication. No video work is part of this run. |
| Team, age, and event attendance | **Unverified** | Team limit is four people. Each entrant must be 18+ and confirm SF on October 6, 2026, or record an AI Worth Using segment before the event. |
| Verification and one-click availability | **Blocked** | After the image boots and the agent works, the organizer/admin must verify the listing and enable one-click deploy. No verification or one-click deployment is confirmed. |
| Plow build path | **Blocked** | The current official Plow base default is a prohibited old model in this project context. Its viability cannot be assumed, and no fallback or replacement route is authorized here. Validate an approved explicit model route before using Plow. |

## Verified development progress, September 24

Eight focused workflow and preserved experiment tests passed. Real mode was checked with fictional test records only, including a valid review and malformed status rejection. Artifact permissions were checked. The fresh dedicated gateway passed config validation and health on loopback 20789; launcher and installed workflow documentation were present. A later isolated engineering run completed the full prepare, model draft and validate flow through NVIDIA GLM 5.3 in 174.5 seconds. Saved artifacts passed independent validation and were private (0600 in a 0700 directory). Its fictional input exercised the real-mode schema; it was not a real applicant review. The scoped collector read nonzero usage matching the native run metadata. No collaborator interaction or Index submission occurred. The OpenAI generated repository cover is published with source. [Demo recording plan](DEMO.md).

## Dates

The official Luma listing gives these deadlines:

* Submission: **September 28, 2026 at 11:59 pm PT**, which is **September 29, 2026 at 1:59 am CDT (Chicago)**.
* Leaderboard snapshot: **September 30, 2026 at 11:59 pm PT**, which is **October 1, 2026 at 1:59 am CDT (Chicago)**.
* Winner announcement: October 1, 2026.
* AgentCribs event and live demo: October 6, 2026.

The local CLI now supports explicitly attested, minimized real evidence bundles and validates unranked findings. See [WORKFLOW.md](WORKFLOW.md). Operator attestations do not independently verify authority, consent or privacy. No real applicant execution has been verified.

## Smallest launch sequence

1. Confirm the real startup hiring owner, authorized collaborator, role, consent boundary, and human-only disposition boundary.
2. Implement and exercise one OpenClaw 2.0 multiplayer flow with that owner and collaborator. Preserve evidence of the real work performed.
3. Choose an approved explicit model route. Do not rely on the prohibited Plow default.
4. Keep the published MIT repository installable. Use the official bring your own agent path with the scoped client; a public container and admin verification are separate distribution work.
5. Register the agent, schedule usage reporting, and verify a genuine install and reported usage. Ask the organizer/admin for verification and one-click deployment.
6. Record a 60-second-or-longer demo of the real workflow, confirm entrant eligibility and team size, and submit before the Chicago equivalent of the PT deadline.

## Sources

* [Official Luma event](https://luma.com/zhkhsnpa): use case, multiplayer, MIT, 60-second demo, team and age rules, no artificial usage, verification, and dates.
* [Agent Index publish instructions](https://aiworthusing.com/agent-index/publish): Plow or bring-your-own-agent paths, official client usage reporting, registration, public image, verification, and one-click deploy.
* Prior evidence: [experiment history](EXPERIMENT-HISTORY.md), imported from the old repo. It records synthetic results only.

## Multiplayer and reporting path

Use the dedicated native agent with trusted hiring collaborators. OpenClaw documents multi user sessions, creator/owner attribution and participant history. Each person needs a distinct authenticated identity; two tabs using the same owner token do not prove two users. Keep the gateway private. Session visibility does not isolate tools, files or credentials. Select the actual collaborator and channel before configuring admission. [OpenClaw multi user mode](https://docs.openclaw.ai/concepts/multi-user).

The official bring your own agent route permits the existing scoped collector. Obtain the Plow credential through the official login, register, verify an accepted report, then enable reporting every five minutes. No credentials or reporting schedule have been activated. Obtain admin verification and a working public container for the documented one click deployment flow. Do not switch to the Plow base merely to obtain a listing. [Publish instructions](https://aiworthusing.com/agent-index/publish).

## Build decisions, September 24

Use Codex Sol for scoped implementation and Luna for bounded research, with at most two concurrent workers. The cover in `assets/recruiter-cover.png` was generated using OpenAI's built-in image tool; its exact model version was not exposed. Runtime inference stays on the existing explicit NVIDIA route until a different route and its access are deliberately configured.

Current official OpenAI documentation lists GPT-6 Astra, Sol and Luna, GPT Image 2.5 Flare and Sunburst, and GPT-Live 1. Flare targets speed; Sunburst targets image quality. These are available product names, not proof of this account's API access. No additional voice or agent platform integration is needed to finish this entry. Sources: [model catalog](https://developers.openai.com/api/docs/models/all), [image guidance](https://developers.openai.com/api/docs/guides/image-prompting).

[DevDay is September 29](https://openai.com/index/devday-2026/), after the September 28 submission deadline. Submit with current products. Evaluate later announcements only if they solve a measured problem without risking the entry; no unannounced capability is a dependency.

Essential verification only: fresh install and restart, useful owner task, genuine collaborator interaction with access boundaries, one accepted correctly attributed usage report, and signed out listing/video access. A green unit test or generated cover satisfies none of those live gates.

## Current pre-video finish line

The existing folder contains recruiting research and fictional experiments, but no actual hiring queue or collaborator setup. The user confirmed that these may not have been created. An engineering check cannot create genuine hiring authority or another human participant.

Completed: native live workflow check, isolated usage preview, verification-state publication guard, local Docker startup and identity-preserving restart. [Container instructions](CONTAINER.md). The standalone GLM code-review request hit its output cap and returned no usable review; no fallback or retry ran. The separate native GLM workflow completed and was independently checked.

Remaining: identify an actual recruiting job and authorized collaborator/channel; obtain the official Plow login credential for the Index; register and verify accepted real usage; obtain organizer verification and one click availability. No Plow token or scoped Index registration file was found in the documented paths. Public source and container preparation can proceed independently. Stop before video.
