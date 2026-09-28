# Roletrace offline verification

Verified September 28, 2026 against the working tree. This record covers deterministic local checks only. No provider call, applicant data, live hiring workflow, usage report, publication, deployment, or external action was performed.

## Fictional real-contract example

`examples/roletrace/` contains a deliberately small before/after exercise for the real-mode JSON contracts. Every role, candidate, source, evidence statement, attestation, and identifier is fictional. The `mode: real` field selects the real-mode schema; it is not evidence of real authority, real consent, real data, or a real hiring owner.

The response JSON files are manually authored fixtures, not model outputs. They contain no score, tier, rank, ordering, recommendation, or disposition. The before and after files preserve the same role, criterion, candidate, and evidence IDs. After the accessibility evidence is clarified, `accessibility_testing` changes from `met` to `unknown`; the unrelated `rollback_planning` finding remains unchanged.

## Checks performed

Command:

```sh
/Users/corby/homebrew/bin/python3 -m unittest discover -v
```

Result: 30 tests passed in the offline suite, independently rerun by the primary agent after integration.

The eight checks in `recruiter/test_adversarial.py` establish that the current deterministic code:

- rejects a real-mode `met` finding with no visible evidence ID;
- rejects an evidence ID owned by another candidate;
- rejects real-mode ranking fields at both review and response level;
- rejects a citation to evidence removed by the configured protected-term filter;
- rejects output containing either configured injection marker, `hire_me_now` or `system override`;
- places conflicting evidence text in the serialized input section before the output contract and final procedure boundary;
- rejects false required attestation flags, unsafe or empty pseudonymous IDs, empty authorized sources, unexpected attestation fields, and evidence outside the attested source list; and
- validates both manually authored fixture responses and asserts the intended before/after finding change while IDs and the unrelated finding remain stable.

The same discovery run also passed four pre-existing workflow tests, four experiment tests, and fourteen presentation tests. Presentation coverage includes exact cited excerpts, missing evidence, invalid and incompatible reviews, same-ID text changes, source labels, added and removed evidence, filtered-text withholding, changed narratives, safe Markdown output, compact unchanged comparisons, and immutable output files. New uncited evidence triggers a recheck notice even when finding fields are unchanged. This does not establish semantic correctness of a finding.

The primary agent separately ran the CLI against the fictional before/after pair and inspected the generated correction report. The [saved example](../examples/roletrace/review-after.md) adds an explicit fictional-fixture notice above deterministic renderer output.

## Evidence boundary and remaining limits

These tests demonstrate JSON schema enforcement, exact configured string checks, evidence ownership checks, configured filtering behavior, prompt assembly order, fixture consistency, and preservation of the human-review-required decision value for the exercised cases.

They do not prove that a model will resist prompt injection, follow the prompt, avoid unconfigured protected or identifying information, interpret evidence correctly, or return factually correct findings. They do not prove an attestation is true, a source is authorized in reality, evidence is authentic, missing evidence is complete, or a human decision is fair or lawful. The configured protected patterns and injection markers are narrow lists, not comprehensive detection. Passing offline tests does not establish consent, legal compliance, model quality, live provider behavior, deployment behavior, real applicant use, adoption, or hiring fitness.
