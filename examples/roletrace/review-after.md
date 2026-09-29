> **Fictional walkthrough.** Inputs, attestations and responses are manually authored fixtures. This is deterministic renderer output, not a model run or real applicant review.

# Correction comparison

Comparison checks finding fields and cited evidence bytes. It does not determine whether added or uncited evidence changes factual support.

## Changed source text

### `fictional_candidate` / `evidence_accessibility`

**Previous excerpt:**

> The candidate authored automated accessibility tests for the sample interface and explained the assertions\.

**Current excerpt:**

> Clarification&#58; the candidate reviewed a teammate's accessibility test output; this sample did not establish who authored the tests\.

## Changed findings

- `fictional_candidate` / `accessibility_testing`: status `met` -> `unknown`

## Evidence set changed; finding fields and cited evidence unchanged

Recheck these findings against new, removed, changed, or filtered evidence:

- `fictional_candidate` / `rollback_planning`

## Summary and human question changes

### `fictional_candidate` / Summary

Untrusted draft text changed; it is excluded from this evidence review.

### `fictional_candidate` / Human question

Untrusted draft text changed; it is excluded from this evidence review.

# Roletrace evidence review

Decision: **Human review required**

Validation note: structural validation does not verify that a finding is factually supported.

## Candidate `fictional_candidate`

### Criterion `accessibility_testing`

**Exact criterion:** Authored automated accessibility tests for a web interface

**Status:** `unknown`

**Cited source excerpts:**

- Evidence `evidence_accessibility` from source `fictional_work_sample`

> Clarification&#58; the candidate reviewed a teammate's accessibility test output; this sample did not establish who authored the tests\.

### Criterion `rollback_planning`

**Exact criterion:** Explained a rollback plan for a production change

**Status:** `met`

**Cited source excerpts:**

- Evidence `evidence_rollback` from source `fictional_work_sample`

> The candidate described reverting the release artifact and restoring the prior configuration if monitoring showed errors\.

### Summary

Findings above describe criterion evidence only; no overall candidate recommendation is produced.

### Human question

Does each cited excerpt support its finding, and what authorized evidence would resolve any unknowns?
