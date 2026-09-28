from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from recruiter.cli import render
from recruiter.presentation import render_markdown


def real_bundle(text: str = "Explained the work sample tradeoffs") -> dict:
    return {
        "mode": "real",
        "attestation": {
            "hiring_owner_id": "owner_01",
            "operator_id": "operator_01",
            "authority_to_process": True,
            "data_minimized": True,
            "contains_no_names_contacts_or_resumes": True,
            "authorized_sources": ["work_sample"],
        },
        "role": {
            "id": "role_01",
            "criteria": [{"id": "criterion_01", "text": "Can explain a completed work sample"}],
        },
        "candidates": [
            {
                "id": "candidate_01",
                "evidence": [{"id": "evidence_01", "text": text, "source": "work_sample"}],
            }
        ],
    }


def real_response(status: str = "met", evidence_ids: list[str] | None = None) -> dict:
    if evidence_ids is None:
        evidence_ids = ["evidence_01"] if status != "unknown" else []
    return {
        "reviews": [
            {
                "candidate_id": "candidate_01",
                "criterion_findings": [
                    {"criterion_id": "criterion_01", "status": status, "evidence_ids": evidence_ids}
                ],
                "summary": "The cited source addresses the criterion.",
                "human_review": "What should the hiring owner verify next?",
            }
        ],
        "decision": "human_review_required",
    }


class PresentationTest(unittest.TestCase):
    def test_refuses_invalid_response_before_rendering(self) -> None:
        response = real_response()
        response["decision"] = "hire"
        with self.assertRaisesRegex(ValueError, "current response is invalid"):
            render_markdown(real_bundle(), response)

    def test_unknown_is_explicit_and_has_no_invented_excerpt(self) -> None:
        text = render_markdown(real_bundle(), real_response("unknown"))
        self.assertIn("**Exact criterion:** Can explain a completed work sample", text)
        self.assertIn("**Status:** `unknown`", text)
        self.assertIn("No cited source excerpts.", text)
        self.assertIn("### Human question", text)
        self.assertIn("structural validation does not verify", text)

    def test_untrusted_text_is_escaped_as_inactive_markdown(self) -> None:
        bundle = real_bundle("<script>alert(1)</script> | ![image](https://invalid.example) &#60;img&#62;")
        response = real_response()
        response["reviews"][0]["summary"] = "[click](https://invalid.example)"
        text = render_markdown(bundle, response)
        self.assertNotIn("<script>", text)
        self.assertNotIn("![image]", text)
        self.assertNotIn("[click](", text)
        self.assertNotIn("https://", text)
        self.assertIn("&lt;script&gt;", text)
        self.assertNotIn("&#60;img", text)

    def test_comparison_detects_changed_text_with_same_evidence_id(self) -> None:
        previous = real_bundle("Described a completed work sample")
        current = real_bundle("Explained the work sample tradeoffs")
        text = render_markdown(current, real_response(), previous, real_response())
        self.assertIn("# Correction comparison", text)
        self.assertIn("Described a completed work sample", text)
        self.assertIn("Explained the work sample tradeoffs", text)
        self.assertIn("## Finding fields unchanged; cited evidence or source changed", text)
        self.assertIn("`candidate_01` / `criterion_01`", text)

    def test_comparison_separates_changed_and_unaffected_findings(self) -> None:
        previous_response = real_response("unknown")
        current_response = real_response()
        text = render_markdown(real_bundle(), current_response, real_bundle(), previous_response)
        self.assertIn("## Changed findings", text)
        self.assertIn("status `unknown` -> `met`", text)
        self.assertNotIn("## Unchanged findings and cited evidence", text)

    def test_identical_comparison_has_compact_no_change_summary(self) -> None:
        text = render_markdown(real_bundle(), real_response(), real_bundle(), real_response())
        self.assertIn("No compared evidence, finding fields, summaries, or human questions changed.", text)
        self.assertIn("## Unchanged findings and cited evidence", text)
        self.assertNotIn("## Added evidence", text)
        self.assertNotIn("## Removed evidence", text)
        self.assertLess(text.index("# Correction comparison"), text.index("# Roletrace evidence review"))

    def test_comparison_withholds_filtered_evidence_text(self) -> None:
        previous = real_bundle("52 years confidential previous text")
        current = real_bundle("52 years confidential current text")
        text = render_markdown(current, real_response("unknown"), previous, real_response("unknown"))
        self.assertNotIn("confidential previous text", text)
        self.assertNotIn("confidential current text", text)
        self.assertIn("filtered evidence changed; excerpt withheld", text)

    def test_comparison_tracks_source_label_and_narrative_changes(self) -> None:
        previous = real_bundle()
        current = real_bundle()
        previous["attestation"]["authorized_sources"].append("interview")
        current["attestation"]["authorized_sources"].append("interview")
        current["candidates"][0]["evidence"][0]["source"] = "interview"
        current_response = real_response()
        current_response["reviews"][0]["summary"] = "Current summary"
        text = render_markdown(current, current_response, previous, real_response())
        self.assertIn("`work_sample` -> `interview`", text)
        self.assertIn("## Summary and human question changes", text)
        self.assertIn("Current summary", text)

    def test_comparison_tracks_added_and_removed_eligible_evidence(self) -> None:
        previous = real_bundle()
        current = real_bundle()
        previous["candidates"][0]["evidence"].append(
            {"id": "evidence_old", "text": "Previous additional excerpt", "source": "work_sample"}
        )
        current["candidates"][0]["evidence"].append(
            {"id": "evidence_new", "text": "Current additional excerpt", "source": "work_sample"}
        )
        text = render_markdown(current, real_response(), previous, real_response())
        self.assertIn("## Added evidence", text)
        self.assertIn("Current additional excerpt", text)
        self.assertIn("## Removed evidence", text)
        self.assertIn("Previous additional excerpt", text)
        self.assertIn("## Evidence set changed; finding fields and cited evidence unchanged", text)

    def test_added_uncited_evidence_requires_recheck_instead_of_unchanged_label(self) -> None:
        current = real_bundle()
        current["candidates"][0]["evidence"].append(
            {"id": "evidence_02", "text": "New uncited evidence may change support", "source": "work_sample"}
        )
        text = render_markdown(current, real_response(), real_bundle(), real_response())
        self.assertIn("Recheck these findings against new, removed, changed, or filtered evidence", text)
        comparison = text.split("# Roletrace evidence review", 1)[0]
        self.assertNotIn("## Unchanged findings and cited evidence\n\n- `candidate_01`", comparison)

    def test_comparison_requires_same_hiring_owner(self) -> None:
        previous = real_bundle()
        previous["attestation"]["hiring_owner_id"] = "owner_02"
        with self.assertRaisesRegex(ValueError, "hiring owner identities differ"):
            render_markdown(real_bundle(), real_response(), previous, real_response())

    def test_rejects_incomparable_candidate_identity(self) -> None:
        previous = real_bundle()
        previous["candidates"][0]["id"] = "candidate_02"
        with self.assertRaisesRegex(ValueError, "candidate identities differ"):
            render_markdown(real_bundle(), real_response(), previous, {
                "reviews": [{**real_response()["reviews"][0], "candidate_id": "candidate_02"}],
                "decision": "human_review_required",
            })

    def test_rejects_changed_criterion_identity_text(self) -> None:
        previous = real_bundle()
        previous["role"]["criteria"][0]["text"] = "A different criterion"
        with self.assertRaisesRegex(ValueError, "criterion identities or text differ"):
            render_markdown(real_bundle(), real_response(), previous, real_response())

    def test_cli_preserves_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path, response_path, output_path = root / "input.json", root / "response.json", root / "review.md"
            import json

            input_path.write_text(json.dumps(real_bundle()), encoding="utf-8")
            response_path.write_text(json.dumps(real_response()), encoding="utf-8")
            output_path.write_text("existing\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "refusing to replace changed artifact"):
                render(input_path, response_path, output_path)
            self.assertEqual(output_path.read_text(encoding="utf-8"), "existing\n")


if __name__ == "__main__":
    unittest.main()
