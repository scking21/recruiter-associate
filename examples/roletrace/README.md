# Roletrace fictional real-contract fixtures

Read the [original review](review-before.md), then the [correction and revised review](review-after.md). The correction appears first, followed by the full current review and its source excerpts.

These files are an offline schema exercise. Every role, candidate, evidence statement, source, attestation, and identifier is explicitly fictional. The `mode: real` value exercises Roletrace's real-mode input and output contracts; it does not mean the files contain real applicant data or genuine attestations.

The two response files are manually authored fixtures. They are not model outputs and contain no scores, tiers, ranks, recommendations, or hiring decisions.

The before and after inputs intentionally retain the same identifiers. In the after input, `evidence_accessibility` is clarified so it no longer establishes that the candidate authored the accessibility tests. The matching finding therefore changes from `met` to `unknown`. The unrelated rollback criterion and its evidence remain unchanged.

Files:

- `fictional_real_contract_before.json`: fictional input before the evidence clarification.
- `fictional_real_response_before.manual.json`: manually authored valid response for the before input.
- `fictional_real_contract_after.json`: fictional input after the evidence clarification.
- `fictional_real_response_after.manual.json`: manually authored valid response for the after input.

Reproduce the comparison locally from the repository root, without a provider or usage report:

```sh
python3 -m recruiter render --input examples/roletrace/fictional_real_contract_after.json --response examples/roletrace/fictional_real_response_after.manual.json --previous-input examples/roletrace/fictional_real_contract_before.json --previous-response examples/roletrace/fictional_real_response_before.manual.json --output runtime/fictional-walkthrough/review.md
```

The checked-in Markdown adds only a fictional-fixture notice above the generated report. Status changes in the manually authored responses are inputs to this comparison; the renderer does not infer them. It flags changed evidence for human rechecking even when finding fields are unchanged.
