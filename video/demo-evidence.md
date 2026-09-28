# Demo evidence and 85-second recording script

Historical evidence plan for the earlier Recruiter Associate demo. Original brand names, cover paths, and proposed narration below are retained as provenance. The active Roletrace revision is described in `README.md` and `script.json`.

This is a preparation sheet for a visually polished demo. It uses the tracked
OpenAI-generated cover asset and offline, fictional fixtures. Put a persistent
on-screen label on every runtime screen: **CONTROLLED SYNTHETIC WALKTHROUGH**.
The collaborator scene must also say **SIMULATED MULTIPLAYER**. Nothing here
proves a real applicant queue, real hiring authority, real collaborator use,
adoption, usage reporting, legal compliance, or organizer acceptance.

## Asset and evidence boundary

The reusable visual asset is `assets/recruiter-cover.png`, a 1942 x 809 RGB PNG
(SHA-256 `7bde5bd2b20ce90444dbfcee470c0f6e65a80c13e5f8d591261110f1a915b3b1`).
`docs/HACKATHON.md` records that the cover was generated with OpenAI's built-in
image tool and that the exact model version was not exposed. Use the cover for
the opening card, a restrained lower-third, and the closing card. Do not claim
an exact OpenAI image model.

The strongest saved, nonprivate runtime evidence is the fictional minimized
real-mode check under:

```text
runtime/verification-20260924/workspace/inputs/engineering-fixture.json
runtime/verification-20260924/workspace/work/engineering-check/input.real.json
runtime/verification-20260924/workspace/work/engineering-check/response.json
runtime/verification-20260924/workspace/work/engineering-check/validation.json
```

It contains pseudonymous IDs, one work-sample criterion, one evidence sentence,
one cited finding, and `decision: human_review_required`. Its validation is
`valid: true` with no errors. It is a fictional engineering check in the
real-mode contract, not a real applicant review. Show only the sanitized
extracts below, not the whole runtime directory.

The synthetic fixture and guarded prompt are saved at
`runtime/recruiter-demo/input.synthetic.json` and
`runtime/recruiter-demo/guarded.prompt.txt`; no saved synthetic recommendation
response is present there. The six-applicant fixture source is
`experiments/recruiter/fixture.json`. Historical seven-of-seven results are
documented in `docs/EXPERIMENT-HISTORY.md`, but those provider runs were not
rerun during repository extraction and should be presented as historical
synthetic evidence only.

The multiplayer source of truth is `docs/MULTIPLAYER.md`. It describes two
fictional identities, a shared-session correction, and refusal of an unapproved
identity. The underlying local records are retained under
`private/multiplayer/` and `runtime/multiplayer-20260924/`; do not open, quote,
or screen-record their private conversation payloads. The sanitized event card
below is a prepared visual extract grounded in the documented scenario, not a
transcript.

## 85-second script

The narration is about 185 words, suitable for roughly 80 to 90 seconds at a
calm product-demo pace. Keep the lower third visible on all runtime screens:
`SYNTHETIC FIXTURE` and, during the collaborator scene, `SIMULATED MULTIPLAYER`.

| Time | Picture and exact reusable text | Narration |
| --- | --- | --- |
| 0:00–0:08 | Cover asset on a dark title card. Text: `Recruiter Associate` / `Job evidence. Human decisions.` / `CONTROLLED SYNTHETIC WALKTHROUGH` | “Recruiter Associate prepares a cited evidence review for a human hiring owner. This recording uses a controlled synthetic fixture.” |
| 0:08–0:20 | Show a compact role card: `criterion_01: Can explain a completed work sample`; `candidate_01` / `evidence_01`. Text: `No names • no contacts • no resumes` | “The input is minimized to a job criterion and job-related evidence. The IDs are pseudonymous, and the evidence is treated as untrusted data.” |
| 0:20–0:34 | Show the saved response extract, with `evidence_01` highlighted and `human_review_required` in a green status chip. | “The agent cites the evidence that supports the finding, then leaves the decision with the human. It does not hire, reject, contact, score, or rank the applicant.” |
| 0:34–0:47 | Show the saved validation extract: `valid: true`, `errors: []`, `protected_term_hits: []`, `decision: human_review_required`. | “An offline validator checks the response shape, citation ownership, and the human decision boundary. A pass means the contract is valid, not that the evidence is true or that a hiring decision is safe.” |
| 0:47–1:05 | Two-column event card. Left: `OWNER (SIMULATED)` / `Claim: applicant A fixed a Python timeout.` Right: `MANAGER (SIMULATED)` / `Correction: withdraw that claim; request supporting evidence.` | “Now a controlled multiplayer correction. A simulated manager withdraws a claim in the shared session. The recruiter records Python debugging as unverified, keeps the other evidence, and suggests what to request next.” |
| 1:05–1:17 | Show the corrected finding card: `python_debugging: unknown`; `next check: supporting work sample`; `decision: human_review_required`. Add `NO RANKING • NO DISPOSITION`. | “The correction changes the evidence state, not the owner’s authority. The output stays reviewable and cited, while the human retains every disposition.” |
| 1:17–1:25 | Return to cover asset. Text: `Cited evidence` / `Human review` / `Synthetic test only` / `Real use and publication remain separate gates` | “This demonstrates the workflow and its boundaries. Real applicants, real collaborators, accepted usage, and verified publication still require separate evidence.” |

Do not show a sample leaderboard, a fake usage counter, a provider token, a
gateway pairing URL, a private chat transcript, or a candidate score. Do not
describe the simulated manager as a customer, teammate, applicant, or real
user.

## Exact nonprivate extracts

These blocks are safe to paste into a mockup or terminal overlay. They are
copied from the saved fictional engineering check except for the explicit
display labels added around them.

### Input card

```json
{
  "mode": "real",
  "attestation": {
    "hiring_owner_id": "owner_01",
    "operator_id": "operator_01",
    "authority_to_process": true,
    "data_minimized": true,
    "contains_no_names_contacts_or_resumes": true,
    "authorized_sources": ["work_sample"]
  },
  "role": {
    "id": "role_01",
    "criteria": [
      {"id": "criterion_01", "text": "Can explain a completed work sample"}
    ]
  },
  "candidates": [
    {
      "id": "candidate_01",
      "evidence": [
        {
          "id": "evidence_01",
          "text": "Explained the work sample tradeoffs",
          "source": "work_sample"
        }
      ]
    }
  ]
}
```

### Cited output card

```json
{
  "reviews": [
    {
      "candidate_id": "candidate_01",
      "criterion_findings": [
        {
          "criterion_id": "criterion_01",
          "status": "met",
          "evidence_ids": ["evidence_01"]
        }
      ],
      "summary": "Evidence evidence_01 from the authorized work_sample source states the candidate explained the work sample tradeoffs, which addresses the stated criterion of explaining a completed work sample.",
      "human_review": "Hiring owner: does evidence_01 sufficiently establish the quality and completeness of the work sample explanation for criterion_01, or should a follow-up work sample discussion be scheduled?"
    }
  ],
  "decision": "human_review_required"
}
```

### Validation card

```json
{
  "valid": true,
  "mode": "real",
  "synthetic": false,
  "decision": "human_review_required",
  "errors": [],
  "protected_term_hits": [],
  "injection_marker_hits": []
}
```

The runtime validator also records three limitations: configured pattern
checks are bounded; validation checks structure and safety invariants rather
than factual truth, consent, fairness, legal compliance, or hiring fitness;
and a human remains responsible for hiring, rejection, outreach, and
disposition decisions. If space permits, show these as a small `LIMITS` card.

### Simulated multiplayer correction card

This is a nonprivate scripted visual extract, not a saved chat transcript:

```text
OWNER (SIMULATED)
Claim: applicant A fixed a Python timeout.

MANAGER (SIMULATED)
Correction: withdraw that claim; request supporting evidence.

RECRUITER
python_debugging: unknown
retained: other stated evidence
next check: supporting work sample
decision: human_review_required
```

## Offline preparation and validation

All commands below are local and network-free. They do not invoke a provider,
send a message, or publish anything.

Prepare the synthetic guarded prompt:

```sh
cd "/Volumes/1/Hackathons/OpenClaw Recruiter"
python3 -m recruiter prepare \
  --input experiments/recruiter/fixture.json \
  --output-dir runtime/recruiter-demo-video
```

Validate the saved fictional minimized check:

```sh
cd "/Volumes/1/Hackathons/OpenClaw Recruiter"
python3 -m recruiter validate \
  --input runtime/verification-20260924/workspace/work/engineering-check/input.real.json \
  --response runtime/verification-20260924/workspace/work/engineering-check/response.json
```

The expected terminal result is exit code 0 and a report with `valid: true`,
`errors: []`, and `decision: human_review_required`. The first command creates
a fresh ignored runtime prompt and input snapshot. The existing
`runtime/recruiter-demo/guarded.prompt.txt` is an older frozen artifact; the
CLI correctly refuses to overwrite it when the current source differs. The
second command reads the saved response and prints the validation report
without writing an artifact.

## Finish-line checks for the parent recording task

Before calling the video complete, independently verify the rendered duration
is at least 60 seconds, review every frame for private identifiers and
credentials, and verify any intended public or unlisted watch URL from outside
the owner session. A local render, upload, completed processing state, draft,
or scheduled release is not publication evidence. Keep the video claim at
“controlled synthetic walkthrough” until genuine use and the publication gate
are independently verified. If the current signed-out Agent Index screenshot
is shown, label it as listing status only; do not attribute its active-user or
active-day counter to this synthetic run or call it broad adoption.
