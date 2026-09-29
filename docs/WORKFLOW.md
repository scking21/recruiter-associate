# Roletrace evidence review workflow

Real mode prepares and validates a minimized evidence review. It does not call a model, contact anyone, or make a hiring decision. Keep inputs and outputs outside tracked source.

## Conversational intake

Start with one owner-stated criterion and one short, authorized work-sample excerpt. The agent collects only missing authorization, minimization, and source assertions before accepting real evidence, then assigns neutral review-local IDs and builds the JSON. Users need not learn the schema. IDs are labels, not verified identities. The actual owner must authorize any shared room, collaborators, and review scope. Keep all hiring decisions human.

Preserve supplied valid IDs and criterion wording. Ask about ambiguous attribution rather than guessing. Each correction creates a new review version with the changed evidence and affected finding identified; validate before presenting it. See the deployed skill for the intake sequence and the [pilot protocol](PILOT.md) for real-user evaluation.

The JSON below is the internal workflow contract, not an onboarding form.

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
  "role": {"id": "role_01", "criteria": [{"id": "criterion_01", "text": "Job related criterion stated by the hiring owner"}]},
  "candidates": [{"id": "candidate_01", "evidence": [{"id": "evidence_01", "text": "Minimized job evidence only", "source": "work_sample"}]}]
}
```

IDs use lowercase letters, digits, underscores, or hyphens, start with a letter or digit, and contain at most 64 characters. Do not include names, contacts, resumes, credentials, expected answers, or extra fields. Every evidence source must appear in `authorized_sources`. Pattern filtering is bounded and is not comprehensive privacy, protected trait, or proxy detection.

```sh
umask 077
./recruiter-tool prepare --input inputs/input.real.json --output-dir work/review
./recruiter-tool validate --input work/review/input.real.json --response work/review/response.json --output work/review/validation.json
./recruiter-tool render --input work/review/input.real.json --response work/review/response.json --output work/review/review.md
```

Preparation writes `input.real.json` and `evidence-review.prompt.txt` with owner only permissions. In the installed OpenClaw workspace, the agent reads the prompt, drafts `response.json` in the current conversation without invoking a separate provider or network tool, and validates it before presenting findings. A valid response contains complete criterion findings, candidate owned citations, and `human_review_required`. Its structured fields contain no scores, tiers, rankings, ordering, recommendations, outreach, or dispositions. Legacy free-text fields are untrusted and are never included in the rendered review. The hiring owner retains every decision.

## Readable output and corrections

`render` validates the input and response before creating Markdown with the exact criteria, statuses, cited excerpts, summary, and human follow-up question. It does not call a model. Review text is rendered as text rather than executable HTML or Markdown supplied by evidence. Structural validation is not factual verification; a human still checks whether the cited evidence supports each finding.

For a correction, prepare and validate a new version in a new directory, then compare it with the exact earlier files:

```sh
./recruiter-tool render --input work/review_02/input.real.json --response work/review_02/response.json --previous-input work/review/input.real.json --previous-response work/review/response.json --output work/review_02/review.md
```

Both previous-file arguments are required together. The comparison separates source changes from finding changes and rejects incompatible identities. Old files are retained; existing output with different content is not overwritten. Compare only reviews from the same authorized conversation. See the [fictional walkthrough](../examples/roletrace/README.md) and [bounded verification](VERIFICATION.md). These examples are manually authored offline artifacts, not recorded model responses or real hiring activity.

Synthetic compatibility remains available:

```sh
python3 -m recruiter prepare --input experiments/recruiter/fixture.json --output-dir runtime/recruiter-demo
```

Real-mode responses should omit `summary` and `human_review`. The renderer supplies fixed neutral summary and human-check text. Legacy responses remain readable, but their narrative fields are excluded from both the current review and correction comparison. Never present raw model narrative or response JSON as the validated review; present only the renderer output. This closes the narrative recommendation channel, not arbitrary instructions in quoted source evidence or criteria.
