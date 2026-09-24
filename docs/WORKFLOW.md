# Recruiter evidence review workflow

Real mode prepares and validates a minimized evidence review. It does not call a model, contact anyone, or make a hiring decision. Keep inputs and outputs outside tracked source.

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
```

Preparation writes `input.real.json` and `evidence-review.prompt.txt` with owner only permissions. In the installed OpenClaw workspace, the agent reads the prompt, drafts `response.json` in the current conversation without invoking a separate provider or network tool, and validates it before presenting findings. A valid response contains complete criterion findings, candidate owned citations, and `human_review_required`. It contains no scores, tiers, rankings, ordering, recommendations, outreach, or dispositions. The hiring owner retains every decision.

Synthetic compatibility remains available:

```sh
python3 -m recruiter prepare --input experiments/recruiter/fixture.json --output-dir runtime/recruiter-demo
```
