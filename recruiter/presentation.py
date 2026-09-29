"""Deterministic Markdown presentation for validated real-mode reviews."""

from __future__ import annotations

import html
from typing import Any

from .workflow import _filtered_candidates, bundle_mode, validate_response


def _validated_real(bundle: dict[str, Any], response: dict[str, Any], label: str) -> None:
    if bundle_mode(bundle) != "real":
        raise ValueError(f"{label} input must use mode real")
    report = validate_response(bundle, response)
    if not report["valid"]:
        raise ValueError(f"{label} response is invalid: {'; '.join(report['errors'])}")


def _escape(value: str) -> str:
    """Escape untrusted text while preserving its rendered characters."""
    escaped = html.escape(value, quote=False).replace("\\", "\\\\")
    for character in "`*_{}[]#+-.!|":
        escaped = escaped.replace(character, f"\\{character}")
    return escaped.replace(":", "&#58;").replace("@", "&#64;")


def _quote(value: str) -> list[str]:
    return [f"> {_escape(line)}" if line else ">" for line in value.split("\n")]


def _reviews(response: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {review["candidate_id"]: review for review in response["reviews"]}


def _findings(review: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {finding["criterion_id"]: finding for finding in review["criterion_findings"]}


def _evidence(bundle: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    return {
        candidate["id"]: {item["id"]: item for item in candidate["evidence"]}
        for candidate in _filtered_candidates(bundle)
    }


def _all_evidence(bundle: dict[str, Any]) -> dict[str, dict[str, dict[str, Any]]]:
    return {
        candidate["id"]: {item["id"]: item for item in candidate["evidence"]}
        for candidate in bundle["candidates"]
    }


def _require_comparable(current: dict[str, Any], previous: dict[str, Any]) -> None:
    if current["role"]["id"] != previous["role"]["id"]:
        raise ValueError("current and previous role identities differ")
    if current["attestation"]["hiring_owner_id"] != previous["attestation"]["hiring_owner_id"]:
        raise ValueError("current and previous hiring owner identities differ")
    current_candidates = {candidate["id"] for candidate in current["candidates"]}
    previous_candidates = {candidate["id"] for candidate in previous["candidates"]}
    if current_candidates != previous_candidates:
        raise ValueError("current and previous candidate identities differ")
    current_criteria = {criterion["id"]: criterion["text"] for criterion in current["role"]["criteria"]}
    previous_criteria = {criterion["id"]: criterion["text"] for criterion in previous["role"]["criteria"]}
    if current_criteria != previous_criteria:
        raise ValueError("current and previous criterion identities or text differ")


def _render_review(bundle: dict[str, Any], response: dict[str, Any]) -> list[str]:
    lines = [
        "# Roletrace evidence review",
        "",
        "Decision: **Human review required**",
        "",
        "Validation note: structural validation does not verify that a finding is factually supported.",
    ]
    reviews = _reviews(response)
    evidence = _evidence(bundle)
    for candidate in bundle["candidates"]:
        candidate_id = candidate["id"]
        review = reviews[candidate_id]
        findings = _findings(review)
        lines.extend(["", f"## Candidate `{candidate_id}`"])
        for criterion in bundle["role"]["criteria"]:
            criterion_id = criterion["id"]
            finding = findings[criterion_id]
            lines.extend(
                [
                    "",
                    f"### Criterion `{criterion_id}`",
                    "",
                    f"**Exact criterion:** {_escape(criterion['text'])}",
                    "",
                    f"**Status:** `{finding['status']}`",
                    "",
                    "**Cited source excerpts:**",
                ]
            )
            if not finding["evidence_ids"]:
                lines.extend(["", "No cited source excerpts."])
            for evidence_id in finding["evidence_ids"]:
                item = evidence[candidate_id][evidence_id]
                lines.extend(["", f"- Evidence `{evidence_id}` from source `{item['source']}`", ""])
                lines.extend(_quote(item["text"]))
        lines.extend(["", "### Summary", ""])
        lines.append("Findings above describe criterion evidence only; no overall candidate recommendation is produced.")
        lines.extend(["", "### Human question", ""])
        lines.append("Does each cited excerpt support its finding, and what authorized evidence would resolve any unknowns?")
    return lines


def _render_comparison(
    bundle: dict[str, Any],
    response: dict[str, Any],
    previous_bundle: dict[str, Any],
    previous_response: dict[str, Any],
) -> list[str]:
    current_reviews, previous_reviews = _reviews(response), _reviews(previous_response)
    current_evidence, previous_evidence = _evidence(bundle), _evidence(previous_bundle)
    current_all, previous_all = _all_evidence(bundle), _all_evidence(previous_bundle)
    changed_findings: list[str] = []
    unchanged_with_source_changes: list[str] = []
    unchanged_with_evidence_set_changes: list[str] = []
    unaffected_findings: list[str] = []
    source_changes: list[tuple[str, str, str, str]] = []
    source_label_changes: list[str] = []
    added_evidence: list[tuple[str, str, str]] = []
    removed_evidence: list[tuple[str, str, str]] = []
    withheld_changes: list[str] = []
    narrative_changes: list[tuple[str, str]] = []

    for candidate in bundle["candidates"]:
        candidate_id = candidate["id"]
        current_findings = _findings(current_reviews[candidate_id])
        old_findings = _findings(previous_reviews[candidate_id])
        candidate_evidence_changed = current_all[candidate_id] != previous_all[candidate_id]
        old_items = previous_evidence[candidate_id]
        changed_source_ids: set[str] = set()
        current_items = current_evidence[candidate_id]
        for evidence_id, item in current_items.items():
            old_item = old_items.get(evidence_id)
            if old_item is None:
                added_evidence.append((candidate_id, evidence_id, item["text"]))
                continue
            if old_item["text"] != item["text"]:
                source_changes.append((candidate_id, evidence_id, old_item["text"], item["text"]))
                changed_source_ids.add(evidence_id)
            if old_item["source"] != item["source"]:
                source_label_changes.append(
                    f"`{candidate_id}` / `{evidence_id}`: `{old_item['source']}` -> `{item['source']}`"
                )
                changed_source_ids.add(evidence_id)
        for evidence_id, item in old_items.items():
            if evidence_id not in current_items:
                removed_evidence.append((candidate_id, evidence_id, item["text"]))

        current_withheld = set(current_all[candidate_id]) - set(current_items)
        previous_withheld = set(previous_all[candidate_id]) - set(old_items)
        for evidence_id in sorted(current_withheld | previous_withheld):
            if evidence_id not in previous_withheld:
                withheld_changes.append(f"`{candidate_id}` / `{evidence_id}`: filtered evidence added")
            elif evidence_id not in current_withheld:
                withheld_changes.append(f"`{candidate_id}` / `{evidence_id}`: filtered evidence removed or became eligible")
            elif current_all[candidate_id][evidence_id] != previous_all[candidate_id][evidence_id]:
                withheld_changes.append(f"`{candidate_id}` / `{evidence_id}`: filtered evidence changed")
        for criterion in bundle["role"]["criteria"]:
            criterion_id = criterion["id"]
            current_finding, old_finding = current_findings[criterion_id], old_findings[criterion_id]
            current_signature = (current_finding["status"], frozenset(current_finding["evidence_ids"]))
            old_signature = (old_finding["status"], frozenset(old_finding["evidence_ids"]))
            label = f"`{candidate_id}` / `{criterion_id}`"
            if current_signature == old_signature:
                if changed_source_ids.intersection(current_finding["evidence_ids"]):
                    unchanged_with_source_changes.append(label)
                elif candidate_evidence_changed:
                    unchanged_with_evidence_set_changes.append(label)
                else:
                    unaffected_findings.append(label)
            else:
                changes: list[str] = []
                if old_finding["status"] != current_finding["status"]:
                    changes.append(f"status `{old_finding['status']}` -> `{current_finding['status']}`")
                if frozenset(old_finding["evidence_ids"]) != frozenset(current_finding["evidence_ids"]):
                    changes.append(
                        f"evidence `{', '.join(old_finding['evidence_ids']) or 'none'}` -> "
                        f"`{', '.join(current_finding['evidence_ids']) or 'none'}`"
                    )
                changed_findings.append(f"{label}: {'; '.join(changes)}")

        current_review, old_review = current_reviews[candidate_id], previous_reviews[candidate_id]
        for field, label in (("summary", "Summary"), ("human_review", "Human question")):
            if current_review.get(field) != old_review.get(field):
                narrative_changes.append((candidate_id, label))
    has_changes = any(
        (
            source_changes,
            source_label_changes,
            added_evidence,
            removed_evidence,
            withheld_changes,
            changed_findings,
            unchanged_with_source_changes,
            unchanged_with_evidence_set_changes,
            narrative_changes,
        )
    )
    lines = [
        "# Correction comparison",
        "",
        "Comparison checks finding fields and cited evidence bytes. It does not determine whether added or uncited evidence changes factual support.",
    ]
    if not has_changes:
        lines.extend(["", "No compared evidence, finding fields, summaries, or human questions changed."])
    if source_changes:
        lines.extend(["", "## Changed source text"])
        for candidate_id, evidence_id, old_text, current_text in source_changes:
            lines.extend(["", f"### `{candidate_id}` / `{evidence_id}`", "", "**Previous excerpt:**", ""])
            lines.extend(_quote(old_text))
            lines.extend(["", "**Current excerpt:**", ""])
            lines.extend(_quote(current_text))
    if added_evidence:
        lines.extend(["", "## Added evidence"])
        for candidate_id, evidence_id, current_text in added_evidence:
            lines.extend(["", f"### `{candidate_id}` / `{evidence_id}`", ""])
            lines.extend(_quote(current_text))
    if removed_evidence:
        lines.extend(["", "## Removed evidence"])
        for candidate_id, evidence_id, old_text in removed_evidence:
            lines.extend(["", f"### `{candidate_id}` / `{evidence_id}`", ""])
            lines.extend(_quote(old_text))
    if source_label_changes:
        lines.extend(["", "## Changed source labels", "", *[f"- {item}" for item in source_label_changes]])
    if withheld_changes:
        lines.extend(["", "## Filtered evidence changes", "", *[f"- {item}; excerpt withheld" for item in withheld_changes]])
    if changed_findings:
        lines.extend(["", "## Changed findings", "", *[f"- {item}" for item in changed_findings]])
    if unchanged_with_source_changes:
        lines.extend(
            [
                "",
                "## Finding fields unchanged; cited evidence or source changed",
                "",
                "Recheck factual support for these findings:",
                "",
                *[f"- {item}" for item in unchanged_with_source_changes],
            ]
        )
    if unchanged_with_evidence_set_changes:
        lines.extend(
            [
                "",
                "## Evidence set changed; finding fields and cited evidence unchanged",
                "",
                "Recheck these findings against new, removed, changed, or filtered evidence:",
                "",
                *[f"- {item}" for item in unchanged_with_evidence_set_changes],
            ]
        )
    if unaffected_findings:
        lines.extend(["", "## Unchanged findings and cited evidence", "", *[f"- {item}" for item in unaffected_findings]])
    if narrative_changes:
        lines.extend(["", "## Summary and human question changes"])
        for candidate_id, label in narrative_changes:
            lines.extend(["", f"### `{candidate_id}` / {label}", "", "Untrusted draft text changed; it is excluded from this evidence review."])
    return lines


def render_markdown(
    bundle: dict[str, Any],
    response: dict[str, Any],
    previous_bundle: dict[str, Any] | None = None,
    previous_response: dict[str, Any] | None = None,
) -> str:
    """Render a validated real review and optional correction comparison."""
    if (previous_bundle is None) != (previous_response is None):
        raise ValueError("previous input and response must be supplied together")
    _validated_real(bundle, response, "current")
    if previous_bundle is not None and previous_response is not None:
        _validated_real(previous_bundle, previous_response, "previous")
        _require_comparable(bundle, previous_bundle)
    if previous_bundle is not None and previous_response is not None:
        lines = _render_comparison(bundle, response, previous_bundle, previous_response)
        lines.extend(["", *_render_review(bundle, response)])
    else:
        lines = _render_review(bundle, response)
    return "\n".join(lines) + "\n"
