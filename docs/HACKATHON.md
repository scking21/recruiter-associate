# Roletrace Hackathon Readiness

This is the selected recruiter route. It supersedes the old Trail priority. The prior recruiter experiment is useful synthetic evidence only; it does not establish a real hiring owner, applicant queue, deployment, multiplayer use, Agent Index reporting, or demand.

## Compliance matrix

| Requirement or gate | State | Evidence and next action |
| --- | --- | --- |
| Real startup hiring use case | **Blocked** | The product must own a real recruiting job for this startup. Identify the hiring owner and the job they authorize the agent to do. |
| OpenClaw 2.0 multiplayer | **Simulation verified; real adoption pending** | Two distinct simulated profiles interacted in one shared session; the correction was retained. See [evidence](MULTIPLAYER.md). The solo builder approved simulation for engineering verification. Real users and usage remain separate. |
| Human hiring authority | **Implemented; human use unverified** | The old synthetic protocol kept every disposition with a human and excluded protected information. Recheck that boundary in the real workflow; synthetic results are not hiring validation. |
| Technical recruiter evidence | **Done in prior experiment** | The old repo records a refined guarded arm passing 7 of 7 synthetic gates. This is not evidence of real users, consent, adoption, or distribution. |
| Public Agent Index listing | **Registered and publicly verified** | [Listing](https://aiworthusing.com/agent-index/recruiter-associate) checked signed out. Scoped report key saved privately. No usage submitted. |
| MIT license and official client reporting | **Registered; real reporting pending** | MIT LICENSE is present and the public repository is created. The vendored official client retains Apache 2.0; actual usage submission and acceptance remain unverified. |
| Genuine usage and installs | **Blocked** | September 28 public Index shows one successful install and 409K tokens attributed to Daniel. This establishes displayed usage, not a real hiring workflow or adoption. The builder confirms no hiring owner or collaborator is available. Use only genuine startup users and collaborators. Artificial usage, fabricated applicants, and self-generated leaderboard activity are prohibited. |
| Demo video, at least 60 seconds | **Roletrace replacement published** | 93.952-second 1080p demo with Brian narration and Roletrace OpenAI cover. Fictional and simulated labels retained. Unlisted `-CKQ7tGdFxE`; signed-out playback and Index embed verified September 28 at 13:00 UTC. See [demo artifacts](DEMO.md). |
| Team, age, and event attendance | **Unverified** | Team limit is four people. Each entrant must be 18+ and confirm SF on October 6, 2026, or record an AI Worth Using segment before the event. |
| Verification and one-click availability | **Publicly verified** | September 28 listing shows Verified and one-click deploy. Outcome-focused copy, Corby King attribution, video, and labeled screenshot are live; WIP badge is absent. |
| Plow build path | **Updated cloud image published and promoted** | [Cloud integration](CLOUD.md) inherits official messaging/reporting. The user approved hosted Plow GLM 5.2 on September 25; fallback is removed. Offline build, config/reporting contract and actual gateway/plugin probe passed in run36174574457. |

## Verified development progress, September 24

Eight focused workflow and preserved experiment tests passed. Real mode was checked with fictional test records only, including a valid review and malformed status rejection. Artifact permissions were checked. The fresh dedicated gateway passed config validation and health on loopback 20789; launcher and installed workflow documentation were present. A later isolated engineering run completed the full prepare, model draft and validate flow through NVIDIA GLM 5.3 in 174.5 seconds. Saved artifacts passed independent validation and were private (0600 in a 0700 directory). Its fictional input exercised the real-mode schema; it was not a real applicant review. The scoped collector read nonzero usage matching the native run metadata. No collaborator interaction or Index submission occurred. The OpenAI generated repository cover is published with source. [Demo recording plan](DEMO.md).

## Dates

The official Luma listing gives these deadlines:

* Submission (extension verified September 28): **September 29, 2026 at 11:59 pm PT**, which is **September 30, 2026 at 1:59 am CDT (Chicago)**.
* Leaderboard snapshot: **September 30, 2026 at 11:59 pm PT**, which is **October 1, 2026 at 1:59 am CDT (Chicago)**.
* Winner announcement: October 1, 2026.
* AgentCribs event and live demo: October 6, 2026.

The local CLI now supports explicitly attested, minimized real evidence bundles and validates unranked findings. See [WORKFLOW.md](WORKFLOW.md). Operator attestations do not independently verify authority, consent or privacy. No real applicant execution has been verified.

## Smallest launch sequence

1. Technical multiplayer simulation is complete. New users supply their actual hiring task and authorized collaborators. Preserve human hiring authority.
2. Verify a genuine external installation and useful shared task; keep engineering simulation excluded from reporting.
3. Hosted route approved: Plow GLM 5.2 with no fallback. Native installs remain NVIDIA GLM 5.3.
4. Keep the published MIT repository installable. Use the official bring your own agent path with the scoped client; a public container and admin verification are separate distribution work.
5. Registration, verification and one-click deployment are complete. After the first genuine task, verify its correctly attributed accepted report. The hosted image inherits automatic reporting; keep native test traffic excluded and do not enable a native schedule for rehearsals.
6. The published 94-second demo and Index attachment are verified. Preserve them. If a real pilot succeeds, prepare a participant-approved outcome summary; a replacement video is optional. Confirm entrant eligibility and team size before the extended deadline.

## Sources

* [Official Luma event](https://luma.com/zhkhsnpa): use case, multiplayer, MIT, 60-second demo, team and age rules, no artificial usage, verification, and dates.
* [Agent Index publish instructions](https://aiworthusing.com/agent-index/publish): Plow or bring-your-own-agent paths, official client usage reporting, registration, public image, verification, and one-click deploy.
* Prior evidence: [experiment history](EXPERIMENT-HISTORY.md), imported from the old repo. It records synthetic results only.

## Multiplayer and reporting path

Use the dedicated native agent with trusted hiring collaborators. OpenClaw documents multi user sessions, creator/owner attribution and participant history. Each person needs a distinct authenticated identity; two tabs using the same owner token do not prove two users. Keep the gateway private. Session visibility does not isolate tools, files or credentials. Select the actual collaborator and channel before configuring admission. [OpenClaw multi user mode](https://docs.openclaw.ai/concepts/multi-user).

The official bring your own agent route permits the existing scoped collector. Obtain the Plow credential through the official login, register, verify an accepted report, then enable reporting every five minutes. Plow login and scoped registration are complete. Reporting remains disabled until genuine usage is available. Obtain admin verification and a working public container for the documented one click deployment flow. Do not switch to the Plow base merely to obtain a listing. [Publish instructions](https://aiworthusing.com/agent-index/publish).

## Build decisions, September 24

Use Codex Sol for scoped implementation and Luna for bounded research, with at most two concurrent workers. The cover in `assets/recruiter-cover.png` was generated using OpenAI's built-in image tool; its exact model version was not exposed. Runtime inference stays on the existing explicit NVIDIA route until a different route and its access are deliberately configured.

Current official OpenAI documentation lists GPT-6 Astra, Sol and Luna, GPT Image 2.5 Flare and Sunburst, and GPT-Live 1. Flare targets speed; Sunburst targets image quality. These are available product names, not proof of this account's API access. No additional voice or agent platform integration is needed to finish this entry. Sources: [model catalog](https://developers.openai.com/api/docs/models/all), [image guidance](https://developers.openai.com/api/docs/guides/image-prompting).

[DevDay is September 29](https://openai.com/index/devday-2026/), now the same day as the extended submission deadline. Submit with the working stack. Evaluate announcements only if they solve a measured problem without risking the entry; no unannounced capability is a dependency.

Essential verification only: fresh install and restart, useful owner task, genuine collaborator interaction with access boundaries, one accepted correctly attributed usage report, and signed out listing/video access. A green unit test or generated cover satisfies none of those live gates.

## Earlier pre-video assessment (superseded by current status below)

The existing folder contains recruiting research and fictional experiments, but no actual hiring queue or collaborator setup. The user confirmed that these may not have been created. An engineering check cannot create genuine hiring authority or another human participant.

Completed: native live workflow check, isolated usage preview, verification-state publication guard, local Docker startup and identity-preserving restart. [Container instructions](CONTAINER.md). The standalone GLM code-review request hit its output cap and returned no usable review; no fallback or retry ran. The separate native GLM workflow completed and was independently checked.

Remaining: identify an actual recruiting job and authorized collaborator/channel; obtain the official Plow login credential for the Index; register and verify accepted real usage; obtain organizer verification and one click availability. No Plow token or scoped Index registration file was found in the documented paths. Public source and container preparation can proceed independently. Stop before video.

Public container publication completed: [package](https://github.com/users/scking21/packages/container/package/recruiter-associate), [successful Linux build/startup](https://github.com/scking21/roletrace/actions/runs/36074530833). Anonymous pull verified. Image digest: `sha256:ba2d8549fd07f67e8fd94113f92774c4379f86f620358c7a675b4c5d1762a92e`. Native arm64 Docker build also passed locally. Verification gateway stopped. Docker cleanup later failed: the internal host disk had only 142 MiB free and Docker Desktop reported unable to start. The container stop and local image removal are unconfirmed; persistent state was not deleted. Native owner gateway 20789 is separate. No reporting schedule, Index registration or video was activated.

## Current status after solo multiplayer verification

The user authorized simulated participants for technical verification, with genuine adoption expected after publication. [MULTIPLAYER.md](MULTIPLAYER.md) records the passed shared-session correction and distinct owner/participant identities. The isolated test gateway was stopped after verification; its state remains marked DO-NOT-REPORT. This does not claim human adoption or actual applicant work.

Plow phone activation succeeded. The public Index listing and its install link were verified without sign-in; native registration produced a private scoped report key. No usage POST or schedule was activated. Registration now works before a usage database exists, without fabricating traffic.

Remaining setup: organizer verification and one-click admission, including confirming this native OpenClaw image meets their hosting contract. The contract URL linked by the official CLI README returned 404, so compatibility is not assumed. The organizer request was posted in the official hackathon support channel on September 24 at 8:46 pm Chicago time: [Discord message](https://discord.com/channels/1519035948191449268/1544106357865586718/1552858713025413120). Verification and image compatibility confirmation remain pending. Genuine user tasks and accepted reports remain pending. Video remains deferred.

Container refresh after the registration fix passed GitHub Actions build/startup/publication in run [36082699740](https://github.com/scking21/roletrace/actions/runs/36082699740). Anonymous manifest access returned HTTP200 for `sha256:65aed9fa2b2bd6d88cb749a467098fc9f5f43c608bb9de32f59e29f8e9152816`. Full image pull was verified for the earlier image; this refresh checked manifest access without consuming local Docker storage.

## Hosted integration, September 25

The organizers confirmed the public image is accessible but requested Plow messaging, automatic per-install reporting, and host-supported credentials; they do not inject NVIDIA_API_KEY. [Direct reply](https://discord.com/channels/1519035948191449268/1544106357865586718/1552884751155863612). The user authorized this integration.

Cloud source is prepared in deploy/cloud using an immutable official Plow base. It inherits messaging, fresh-install registration, persistent install state, and five-minute reporting. A recruiter config wrapper removes the fallback and cross-conversation send tools. The user approved Plow GLM 5.2 with no fallback, and that setting is baked into the hosted image. Native NVIDIA installs are separate. [Cloud instructions and remaining gates](CLOUD.md). [Network-disabled build and actual gateway/plugin probe passed](https://github.com/scking21/roletrace/actions/runs/36174574457) in 1m41s; no cloud model calls, deployment, simulated report, organizer follow-up, or video work has occurred.

Cloud publication run [36175691282](https://github.com/scking21/roletrace/actions/runs/36175691282) passed all offline checks and publication. New public digest: `ghcr.io/scking21/recruiter-associate@sha256:d66103775763b06c969bab68ee175bffec20e6ffa390b54186c6520cc7fdd3a6`. The digest and required integration details were sent to the organizers on September 25 at 1:52 pm Chicago, requesting their fresh hosted reply and separate installer usage verification. No live acceptance claimed.

[Organizer follow-up with published cloud digest](https://discord.com/channels/1519035948191449268/1544106357865586718/1553117041001496658).

## Demo completion, September 28

The user reopened the video step: "complete the video using openai assets". The finished local artifact is `video/output/recruiter-associate-demo.mp4` (86.058667 seconds, 1920×1080, 30 fps, H.264/AAC, 16,314,997 bytes), SHA-256 `0764e33e356a4ba0863e55da3856379946610ecceec3166947276df8c36badf4`. Full decode passed; browser playback advanced with no media error. Sampled frames checked all six scenes. Captions are burned in and supplied as SRT. The existing OpenAI-generated cover is reused; narration is local macOS Samantha, not OpenAI speech. No provider call or artificial usage was generated.

The saved agent response is from the documented fictional engineering test. Fresh offline validation passed; the collaborator sequence is explicitly a summary of the September 24 simulated shared session, not live applicant use.

Live public Index check on September 28 confirmed the verified badge, hosted setup link, and local install link. The site still said "No demo video or screenshots submitted yet." These current observations supersede older organizer-pending entries for those specific gates only.

**Publication verified September 28 at 11:12 UTC:** [YouTube](https://www.youtube.com/watch?v=kbqJ_CwPnss), unlisted, played signed out in Brave Private. The [Index listing](https://aiworthusing.com/agent-index/recruiter-associate) embeds the same ID and played to 33 seconds. Official client updated metadata while preserving install identity; no usage report submitted. Receipt: `video/output/publication-verification.json`.

**Narration replacement, September 28:** user authorized ElevenLabs and Chrome. Brian - Relatable Everyman replaces Samantha. Export: 93.162667 seconds, 1920×1080, H.264/AAC, 19,181,941 bytes; full decode passed. SHA-256 `61f11f83b803226fd27f63280450260b0bab832a9d2c716474385172a3c3a180`. [Replacement YouTube video](https://www.youtube.com/watch?v=pefBDsbXzvU) published unlisted; signed-out playback verified. Index metadata updated preserving install identity and without submitting usage. Current receipt: `video/output/publication-verification.json`; original receipts and MP4 preserved under `video/output/original-samantha`.

Replacement publication and Index embedded playback (42 seconds) verified 2026-09-28T11:56:13Z. Screenshots and current receipt are in `video/output/`.

## Listing and intake improvements, September 28

User approved the Editor’s Choice comparison recommendations and chose public builder name **Corby King**. The live listing now has the outcome-focused description and a labeled fictional evidence-review screenshot at an immutable public GitHub URL. The Index board was verified to show Corby King, Verified, and one-click deploy with the WIP badge removed. No usage was submitted.

The user has no hiring owner or collaborator available. A real-user pilot remains blocked on those participants; no outreach or real applicant processing is authorized by this preparation. See [pilot protocol](PILOT.md). Intake changes are published in commit `63545e2`: the agent assigns neutral review-local IDs, asks only for missing authorization/source information, starts with one criterion and excerpt, and preserves correction versions. Four workflow tests and Python compilation passed. [Run 36422188892](https://github.com/scking21/roletrace/actions/runs/36422188892) passed container build, configuration checks, and actual gateway/plugin startup with network/reporting disabled in 1m52s. Plow accepted and a subsequent public read confirmed the enabled new-install pin `ghcr.io/scking21/recruiter-associate@sha256:5fb6c312f188b043cbf4493927d1b2b3515e480bce45f119dfbabd27dcb42910` at 2026-09-28T12:32:55+00:00. Existing installs keep their images. Fresh hosted review and real-user validation remain unverified; no messages or usage were submitted.

## Accepted display name, September 28

The user-approved side-chat handoff selects **Roletrace**, with suggested tagline “Hiring evidence. Clear sources. Human decisions.” The correction is to choose distinctive hackathon product names rather than generic job titles. Keep the existing `recruiter-associate` technical slug, listing identity, and URLs separate from display-name changes. That learning pass recorded the name; the subsequent user request activated the full rebrand. Domain and trademark availability were not verified in the side chat.

## Roletrace rebrand completed, September 28

User requested “rename everything” and gstack review. Roletrace and “Hiring evidence. Clear sources. Human decisions.” are applied to active source display names, README, prompts, workflow labels, cover, evidence screenshot, video visuals/narration/captions, GitHub description and public Index. [New video](https://www.youtube.com/watch?v=-CKQ7tGdFxE) is published unlisted and verified signed out, with working Index playback at 13:00 UTC. Media hash and provenance are in [DEMO.md](DEMO.md).

Source commit `f85cd72` passed four workflow tests. The local installed config and two prompt headings were migrated with backups; independent parsed comparison confirmed all other configuration remained unchanged, and isolated OpenClaw config validation passed using Node 24.16.0. No gateway restart or live inference is claimed. Cloud run `36424027061` passed build, offline contract and actual gateway/plugin startup checks. The Roletrace image was anonymously inspected, promoted, and read back enabled; see [CLOUD.md](CLOUD.md).

At this earlier checkpoint, compatibility exceptions included the repository/Index slug, package coordinate, CLI/environment/skill IDs and filesystem checkout names remain `recruiter-associate` or recruiter-based so existing links, reporting and installs continue working. Existing third-party hosted instances keep their prior images. The internal Plow catalog label remains Recruiter associate; its owner CLI updates the public Index name but exposes no catalog-name migration. Historical videos, original assets and verification records retain their original names. No listing was recreated and no identity, traffic or real-user outcome was invented.

[Scoped gstack review](designs/roletrace-review.md) covered CEO, design, DX, engineering and code-review methods. Findings on display labels, current native state and media consistency were addressed; package migration risk is avoided through compatibility IDs. This is not a full autoplan certification: the outside Claude review could not run because Claude was unauthenticated. The real-user pilot is still prepared, not run, because the user has no hiring owner or collaborator.

## Evidence review improvements, September 28

The user directed work toward controllable product and submission improvements and explicitly authorized delegation with independent verification. Roletrace now has an offline `render` command that validates a response before presenting exact criteria, cited source excerpts and human follow-up questions. Corrections compare the prior and current saved reviews, preserve old artifacts, separate changed evidence from changed findings, and flag new or changed evidence for rechecking. It does not infer whether a finding is true.

Native and cloud skill instructions use the renderer, group missing intake questions and keep resolved assertions. The repository opens with a [readable correction walkthrough](../examples/roletrace/README.md), explicitly labeled as manually authored fictional fixtures. Eight new adversarial checks and fourteen presentation tests supplement the existing eight tests; the primary independently ran all 30 successfully. [Verification scope](VERIFICATION.md).

Two native delegated assignments were integrated and independently reviewed using the gstack critical/informational checklist. Review found and fixed same-ID text changes, filtered comparison excerpts, and misleading unchanged-finding labels when contradictory evidence was added. Final native reviewer found no remaining fixable defect in its scope; primary separately checked source, fixture bytes, CLI output and the full suite. Claude outside review remains unavailable because it is signed out; no full cross-model gstack certification is claimed.

Release verified September 28 at 18:55 UTC: source `ff0e07a`, recovery packaging `a7ef7b7`, and [cloud run36468209995](https://github.com/scking21/roletrace/actions/runs/36468209995) passed source tests, image build, offline configuration/reporting checks, packaged presentation tests and actual gateway/plugin startup with networking disabled. Anonymous registry inspection confirmed the inherited runtime layers, entrypoint, identity and approved model. The enabled new-install image pin was promoted and independently read back as `sha256:8f420308e79462dc189de798b11129396d901933dd60ec3f95fc34acfdebc0dc`; the public Index blurb now describes evidence corrections. Existing hosted instances retain their previous images. See [registry recovery provenance](CLOUD.md).

The local installed CLI and skill were updated with a backup under `runtime/review-output-backup-20260928-134822`; configuration bytes were unchanged. Its offline renderer output matched the public example after the example's fictional notice. No running agent turn or restart was needed or claimed. The existing video and its verified publication remain intact. No model benchmark, outreach or artificial usage was generated. Genuine adoption is a separate limitation, not a prerequisite to these improvements.

## Public-name verification, September 28

Repository renamed to [scking21/roletrace](https://github.com/scking21/roletrace), retaining repository ID `R_kgDOUp-kkw`; the old Git URL resolves to the same HEAD. Local origin, installation instructions, OCI source labels, reporting metadata and current source/video-description links use the new URL. Workflows explicitly retain the existing GHCR package coordinate. [Post-rename run 36469962654](https://github.com/scking21/roletrace/actions/runs/36469962654) passed source tests, container/configuration checks, offline gateway startup and publication. Anonymous registry read verified `sha256:d87f228978afb721f23d5295567eca6a8b4d7d94da823d7e38bc47c4aa52e755` with the new source URL, Roletrace display name and unchanged identity/model. The enabled Index image remains the already verified `8f420308...` release; this check did not replace running agents.

Live Agent Index card, detail heading, video title and screenshot use Roletrace; repository, install and screenshot URLs were updated and read back. The stable Index slug remains `recruiter-associate`. Plow's separate internal catalog label remains “Recruiter associate”; the owner CLI exposes no catalog-name migration. This is an unresolved platform label, not a completed rename.

YouTube's current unlisted demo [-CKQ7tGdFxE](https://www.youtube.com/watch?v=-CKQ7tGdFxE) has a Roletrace title, description, thumbnail and closing-card branding. Studio confirmed saved source-link correction to `github.com/scking21/roletrace`; the public watch page read back that description and playback advanced to 0:12. Its rendered closing card still contains the old GitHub URL, which redirects correctly; source for future renders is corrected. This metadata audit did not repeat the earlier signed-out publication check. Earlier unlisted uploads `pefBDsbXzvU` and `kbqJ_CwPnss` were renamed “Roletrace | Earlier demo (superseded)” and “Roletrace | Original demo (superseded)”, with descriptions linking the current demo and new source URL. Their historical footage and uploaded filenames are unchanged. The unrelated Arrastra Relay video is a different project.
