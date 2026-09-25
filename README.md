# Recruiter associate

![Recruiter Associate: Job evidence. Human decisions.](assets/recruiter-cover.png)

An OpenClaw recruiter assistant that prepares cited, job related application reviews for a human hiring owner. The human retains hiring decisions and candidate communication.

This is the separate recruiter entry for the [AI Worth Using OpenClaw 2.0 hackathon](https://luma.com/zhkhsnpa). It preserves the refined recruiter experiment and supplies an isolated native OpenClaw installer and scoped Agent Index tooling. It is not yet a verified hackathon submission.

## Run locally

Python 3.10+ is required. Start with the network free recruiter CLI:

```sh
python3 -m recruiter prepare --input experiments/recruiter/fixture.json --output-dir runtime/recruiter-demo
```

For a packaged install, see [Docker instructions](docs/CONTAINER.md). For the dedicated native OpenClaw agent, follow [INSTALL.md](docs/INSTALL.md). It uses its own state and port 20789, the explicit NVIDIA `z-ai/glm-5.3` route, and no fallback. It does not alter the parked Trail agent or your default OpenClaw gateway.

## What is included

- Frozen synthetic recruiter fixture, guarded prompt and deterministic evaluation code under `experiments/recruiter/`.
- Offline prompt preparation and review validation under `recruiter/`. [Real mode](docs/WORKFLOW.md) requires explicit operator attestations and minimized evidence; it provides cited findings without candidate scores or rankings. No real applicant run has been verified.
- Recruiter skill and founder review instructions.
- Native installer with a pinned Python launcher and streaming usage accounting enabled.
- Official Agent Index client and a wrapper limited to this agent's usage store. See [REPORTING.md](docs/REPORTING.md).

Historical experiments reported the refined guarded arm passing seven fixture gates in two consecutive runs. Those provider runs were not repeated during repository extraction. See [experiment history](docs/EXPERIMENT-HISTORY.md). Pattern filtering and synthetic scores do not establish comprehensive privacy protection, fairness, legal compliance or real adoption.

## Hackathon finish line

The [public Agent Index listing](https://aiworthusing.com/agent-index/recruiter-associate) is registered. A [simulated multiplayer check](docs/MULTIPLAYER.md) verified separate profile attribution and a shared review correction. Still required: genuine user tasks and reported usage, an install proven by another operator, organizer verification, and a published video of at least 60 seconds. Synthetic applicants and test runs are excluded from reporting. See [the launch checklist](docs/HACKATHON.md).

The intended multiplayer flow is an authorized hiring owner and collaborator reviewing cited findings and recording their own decisions in a shared OpenClaw conversation. Applicant material is untrusted input. Candidate facing access requires separate isolation and consent; this repository does not expose an owner gateway publicly.

## Data and license

MIT for this project. The vendored official Agent Index client retains its Apache 2.0 license. Only explicitly synthetic applicant fixtures belong in this public repository. Keep resumes, contacts, conversations, credentials and real hiring records outside tracked source. Do not send outreach or make automated hiring dispositions.
