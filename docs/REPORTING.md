# OpenClaw usage reporting

`scripts/recruiter_report.py` is the project wrapper around the vendored Agent
Index client. It has one fixed reporting identity, `recruiter-associate`, and it
requires a state root containing exactly this store:

```text
runtime/openclaw-state/
└── agents/recruiter-associate/agent/openclaw-agent.sqlite
```

The wrapper rejects missing stores and any additional agent directory. This
prevents a preview or report for this entry from silently combining usage from
the operator's other OpenClaw agents.

It also accepts only the approved GLM route model IDs `z-ai/glm-5.3` and
`nvidia/z-ai/glm-5.3`. A different or ambiguous model is refused before any
publication attempt.

## Safe preview

Preview is the default and is read only. It calls the vendored client's
`from_openclaw(days, state)` collector and `merge` formatter. It does not call
the client's authentication, registration, or POST functions, does not read a
credential, and does not write state. The output contains only dates, model
names, and aggregate token counters:

```sh
python3 scripts/recruiter_report.py \
  --state-dir runtime/openclaw-state \
  --days 28
```

The vendored collector reads `transcript_events` from each allowed SQLite
store and counts message usage by local calendar day. Session text and session
identifiers are never included in the output.

## Explicit publication

Publication is a separate, explicit operation:

```sh
python3 scripts/recruiter_report.py \
  --state-dir runtime/openclaw-state \
  --days 28 \
  --report
```

The wrapper scopes the vendored client's state function, token path, and
legacy state path to `runtime/openclaw-state/reporting` without changing the
process `HOME`. It then uses the
client's own report key lookup, API origin validation, authorization header,
and usage POST implementation for the fixed `recruiter-associate` agent. A
report key must already exist there; the report mode never registers an agent or
mints credentials.

Registration is available as a separate explicit mode with fixed public
metadata. It requires `PLOW_AGENT_TOKEN` in the process environment, then
invokes the vendored client's official registration flow:

```sh
export PLOW_AGENT_TOKEN='minted-by-the-approved-Plow-setup'
python3 scripts/recruiter_report.py \
  --state-dir runtime/openclaw-state \
  --register \
  --video-id YOUTUBE_VIDEO_ID
```

`--video-id` is optional and must be an ID, never a URL. The fixed page points
to the public repository and [`docs/INSTALL.md`](INSTALL.md). That install
document describes the local owner operated runtime and does not claim a
multiplayer transport. The helper scopes the client's state function, token
path, legacy state path, and registration identity under
`runtime/openclaw-state/reporting` without changing the process `HOME`.

Verify that `.agent-index.json` is present there before using `--report`.

Do not treat a successful preview as Agent Index acceptance. Before using
`--report`, establish the dedicated OpenClaw runtime, obtain the Plow issued
registration credential through the approved setup, register the public agent
page with the official client, and verify the resulting report key and server
acceptance. No live report was run while preparing this helper.
