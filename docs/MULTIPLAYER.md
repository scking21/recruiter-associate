# Simulated multiplayer verification

Verified September 24, 2026 on OpenClaw 2026.9.5 using NVIDIA `z-ai/glm-5.3`.
This is an engineering simulation, not real applicants, human adoption or qualifying usage.

Two separate WebSocket clients entered the same shared recruiter session through the
documented trusted proxy identity path. The simulated identity provider asserted two
fictional identities, `sim-owner@example.invalid` and `sim-manager@example.invalid`.
OpenClaw recorded distinct profile IDs: the first as creator/owner, the second as a
participant. This tests gateway attribution; it does not verify a real identity provider.

The owner supplied fictional support engineer evidence. The manager then withdrew
the claim that applicant A fixed a Python timeout. The recruiter acknowledged the
withdrawal, changed Python debugging to unverified, retained the other evidence,
and suggested evidence to request. Both turns completed. It did not rank, reject,
contact or make a hiring decision about either fictional applicant.

An unapproved third identity was refused during connection. The shared conversation
was inspected using `sessions.list`; its visibility was `shared`, the owner profile
and participant profile differed, and the participant was labeled `sim-manager`.
`session.members.listEvidence` lists access information and identity labels; its
empty explicit membership list is not the participant-history count.

The test used a separate loopback gateway on port 22789, with no applicant data,
no communication tools, and a `DO-NOT-REPORT` marker. Registration and reporting
were both verified to refuse this state. Do not copy its loopback identity-header
trust into a public deployment. Real shared access needs an authenticated proxy
that overwrites identity headers and admits only trusted collaborators.

Local evidence is retained privately under `private/multiplayer/` and
`runtime/multiplayer-20260924/`. No test conversations or usage were uploaded to
the Index. The separate GLM delegation request for a proposed test fixture failed
with a transport error and returned no usable output; the scenario was prepared
locally. The two actual recruiter responses used the configured GLM runtime.

Sources: [multi user mode](https://docs.openclaw.ai/concepts/multi-user),
[trusted proxy authentication](https://docs.openclaw.ai/gateway/trusted-proxy-auth).

## Re-run on the current build, September 29

Repeated on `main` at `1da0c02` with OpenClaw 2026.9.6 and NVIDIA `z-ai/glm-5.3`, in a fresh isolated state (`runtime/multiplayer-20260929`, `DO-NOT-REPORT`, loopback port 22790, same trusted-proxy identities and prompts). Results:

- Owner turn completed (about 4 minutes) with a cited v1 review: A Python debugging supported by A1, B Python debugging unknown.
- Manager correction completed (about 6 minutes). The agent acknowledged the A1 withdrawal, preserved v1, produced v2 changing A Python debugging to unknown, left B unchanged, and listed evidence to request.
- `sessions.list` showed the session `shared`, owner profile `sim-owner` and a distinct participant profile `sim-manager`.
- An unapproved identity was refused (`NOT_PAIRED`).

The first owner attempt timed out at the 180-second turn limit after two slow provider responses; the passing run used a 600-second limit in this test configuration only. No usage was reported. Evidence is retained privately under `private/multiplayer-20260929/`.

