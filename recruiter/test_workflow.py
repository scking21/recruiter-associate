from __future__ import annotations

import unittest

from recruiter.workflow import build_guarded_prompt, require_real_bundle, validate_response


def real_bundle() -> dict:
    """Return fictional schema test data, never a real applicant or reportable use."""
    return {
        "mode": "real",
        "attestation": {
            "hiring_owner_id": "owner_01", "operator_id": "operator_01",
            "authority_to_process": True, "data_minimized": True,
            "contains_no_names_contacts_or_resumes": True,
            "authorized_sources": ["work_sample"],
        },
        "role": {"id": "role_01", "criteria": [{"id": "criterion_01", "text": "Can explain a completed work sample"}]},
        "candidates": [{"id": "candidate_01", "evidence": [{"id": "evidence_01", "text": "Explained the work sample tradeoffs", "source": "work_sample"}]}],
    }


class WorkflowTest(unittest.TestCase):
    def test_real_mode_requires_explicit_authority(self) -> None:
        bundle = real_bundle()
        bundle["attestation"]["authority_to_process"] = False
        with self.assertRaisesRegex(ValueError, "authority_to_process"):
            require_real_bundle(bundle)

    def test_real_mode_enforces_source_scope_and_excludes_fixture_answers(self) -> None:
        bundle = real_bundle()
        bundle["candidates"][0]["evidence"][0]["source"] = "resume"
        with self.assertRaisesRegex(ValueError, "outside attested authorized_sources"):
            require_real_bundle(bundle)
        bundle = real_bundle()
        bundle["candidates"][0]["evidence"][0]["expected_status"] = "met"
        with self.assertRaisesRegex(ValueError, "fixture answer fields"):
            require_real_bundle(bundle)

    def test_malformed_and_ranked_real_output_fails_without_crashing(self) -> None:
        response = {"reviews": [{"candidate_id": "candidate_01", "criterion_findings": [{"criterion_id": "criterion_01", "status": [], "evidence_ids": [{}]}], "summary": "Review", "human_review": "Check", "tier": "strong"}], "ordered_review": [["candidate_01"]], "decision": "human_review_required"}
        report = validate_response(real_bundle(), response)
        self.assertFalse(report["valid"])
        self.assertTrue(any("invalid status" in error for error in report["errors"]))
        self.assertTrue(any("unsupported fields" in error for error in report["errors"]))
        unsupported = {"reviews": [{"candidate_id": "candidate_01", "criterion_findings": [{"criterion_id": "criterion_01", "status": "met", "evidence_ids": []}], "summary": "Review", "human_review": "Check"}], "decision": "human_review_required"}
        self.assertTrue(any("requires visible evidence" in error for error in validate_response(real_bundle(), unsupported)["errors"]))

    def test_synthetic_contract_remains_compatible(self) -> None:
        bundle = {"synthetic": True, "role": {"criteria": [{"id": "python", "required": True}]}, "candidates": [{"id": "candidate_01", "evidence": [{"id": "c01_e1", "text": "Built a Python service"}]}]}
        response = {"recommendations": [{"candidate_id": "candidate_01", "tier": "strong", "criterion_findings": [{"criterion_id": "python", "status": "met", "evidence_ids": ["c01_e1"]}], "summary": "Evidence supports the criterion.", "human_review": "Review the cited evidence."}], "ordered_review": ["candidate_01"], "decision": "human_review_required"}
        self.assertTrue(validate_response(bundle, response)["valid"])
        self.assertIn("synthetic applications", build_guarded_prompt(bundle))


if __name__ == "__main__":
    unittest.main()
