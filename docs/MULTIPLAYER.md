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
