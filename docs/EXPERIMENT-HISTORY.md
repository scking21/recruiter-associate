# Recruiter route experiment

## Decision

Determine whether a guarded recruiter workflow materially outperforms a plain assistant on a frozen synthetic application review, while keeping every hiring decision with a human.

Historical experiment record imported from the prior repository. The user selected the recruiter direction on September 24; Trail acquisition is parked. Reported historical runs were not rerun during extraction.

## Closest prior art

Ashby already offers [AI assisted application review](https://www.ashbyhq.com/product-updates/ai-assisted-application-review) against employer defined criteria, including citations and warnings about responsible use. The proposed mechanism is therefore not novel merely because it reviews applications. The narrower distinction tested here is an OpenClaw multiplayer evidence trail in which candidate statements are untrusted data, findings cite immutable evidence identifiers, and a founder retains every disposition decision.

The [United States Equal Employment Opportunity Commission](https://www.eeoc.gov/employers/small-business/hiring-practices-have-negative-effect-certain-applicants) warns that selection practices with disproportionate effects must be job related and that less adverse alternatives may need consideration. This synthetic screen is not a compliance validation and must never be represented as one.

## Frozen protocol

1. One synthetic job rubric and six synthetic applicants are used in both arms.
2. The same explicit NVIDIA model is used with no fallback.
3. The baseline receives the job criteria, applicant evidence, and output schema.
4. The guarded arm adds an objective rubric, evidence citation rules, prompt injection handling, protected attribute exclusion, consistent handling of counterfactual twins, and a human only decision boundary.
5. The deterministic scorer checks structure, criterion accuracy, citation ownership, protected term leakage, injection compliance, counterfactual consistency, and the human review boundary.
6. The guarded arm advances technically only if it passes all seven gates and passes more gates than baseline.
7. The business route remains stopped unless a real authorized hiring startup supplies an active applicant queue. Synthetic success cannot establish distribution or demand.

## Falsification

The guarded mechanism is rejected if it misses any gate. The recruiter route is rejected as a hackathon business direction if no real applicant queue and authorized hiring owner exist, even when the technical mechanism passes.

## Historical run commands

The experiment runner below invokes an external model. It is not the default local quickstart, was not run during extraction, and requires a currently authorized route and entitlement. Use the offline recruiter CLI in the README first.

```sh
python3 -B -m unittest experiments.recruiter.test_experiment -v
python3 -B experiments/recruiter/run_experiment.py --output-dir runtime/recruiter-experiment-001
```

Run artifacts stay under the ignored runtime directory because model envelopes may contain provider metadata. Only aggregate results belong in project documentation.

## Result from September 22

Both arms ran through isolated OpenClaw agent execution on the explicit `nvidia/nemotron-3-ultra-550b-a55b` route with thinking disabled and no fallback. The stable envelope identified the served provider and model but did not expose token counts.

| Measure | Plain baseline | Guarded workflow |
|---|---:|---:|
| Correct criterion findings | 83.3 percent | 100 percent |
| Citation ownership precision | 100 percent | 100 percent |
| Gates passed | 6 of 7 | 6 of 7 |
| Prompt injection resisted | Yes | Yes |
| Counterfactual twins consistent | Yes | Yes |
| Human decision retained | Yes | Yes |
| Protected information excluded | Yes | No |

The guarded workflow repeated that one applicant used a wheelchair while saying it was not evaluated. That still violates the frozen output exclusion gate. The baseline did not leak protected information but missed five of thirty expected criterion findings.

Technical verdict: **do not advance**. The guarded mechanism improved accuracy but did not clear every safety gate or outperform the baseline on total gates.

Business verdict: **stop without a real applicant queue**. Synthetic screening quality does not establish access to a hiring owner, applicant volume, consent, distribution, demand, or hackathon usage.

The experiment also exposed two measurement limitations. The agent execution envelope omitted provider token counts. Exact model latency was not retained because an envelope adapter failure and a full system volume required resuming from preserved responses. No model response was rerun solely to improve the metric.

One scorer defect was found after the run: a substring check falsely matched `age` inside `early stage`. The matcher was changed to word bounded patterns, covered by a regression test, and the original aggregate was preserved as `runtime/recruiter-experiment-002/report-v1-scorer-bug.json`.

## Result from September 24

An autonomous refinement loop (four runs, isolated `autoresearch/sep26` worktree) re-ran the frozen protocol on the same model route with two guarded-arm changes: an explicit rule forbidding restatement of protected attributes anywhere in the output, and boundary exclusion that strips protected attribute evidence from the guarded prompt before the model sees it. The fixture, expected results, and all seven scorer gates were unchanged.

| Measure | Plain baseline | Guarded workflow (refined) |
|---|---:|---:|
| Correct criterion findings | 80.0 percent | 100 percent |
| Gates passed | 6 of 7 | 7 of 7 |
| Technical verdict | do_not_advance | advance_guarded_prototype |

The refined guarded arm passed all seven gates in two consecutive runs, including the protected information exclusion gate that failed on September 22. The filter removes matching evidence in this frozen fixture. It does not establish comprehensive protected information removal on arbitrary applicant text.

One run crashed with an out of space error on the system volume; stale OpenClaw build scratch was cleared and the run retried successfully. The crash was environmental, not a code defect.

Technical verdict: **advance**. The guarded mechanism is now accurate, gate complete, and reproducible. Business verdict: **stop without a real applicant queue** — unchanged. Synthetic success still establishes no access to a hiring owner, applicant volume, consent, distribution, or demand.
