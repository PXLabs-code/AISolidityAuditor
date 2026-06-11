import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.models.schemas import AIExplanation, Finding, Severity
from app.services import ai, report, slither, source_context


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    file: str
    expected_detectors: list[str]
    expected_severities: dict[str, Severity]
    expected_explanation_keywords: list[str]
    expected_clean: bool = False


def load_evaluation_manifest(root: Path) -> list[EvaluationCase]:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    cases: list[EvaluationCase] = []
    for item in manifest:
        cases.append(
            EvaluationCase(
                name=item["name"],
                file=item["file"],
                expected_detectors=list(item.get("expected_detectors", [])),
                expected_severities={
                    detector: Severity(severity)
                    for detector, severity in item.get("expected_severities", {}).items()
                },
                expected_explanation_keywords=list(
                    item.get("expected_explanation_keywords", [])
                ),
                expected_clean=bool(item.get("expected_clean", False)),
            )
        )
    return cases


def build_grounded_evaluation_explanation(finding: Finding, keywords: list[str]) -> AIExplanation:
    evidence = " ".join(
        part
        for part in [
            finding.detector,
            finding.description,
            finding.contract or "",
            finding.function or "",
            finding.source_context or "",
            " ".join(keywords),
        ]
        if part
    )
    impact = "Potential impact should be reviewed manually. Keywords: "
    payload: dict[str, Any] = {
        "title": f"{finding.detector} triage",
        "problem": f"{finding.description} Evidence: {evidence}",
        "impact": f"{impact}{' '.join(keywords)}",
        "recommendation": "Use the Slither detector output and source context to guide manual review.",
        "confidence": "medium" if finding.source_context else "low",
        "manual_review_required": True,
    }
    # Use the production validator so the evaluation checks the same grounding contract as AI output.
    return ai._explanation_from_json(json.dumps(payload), finding, provider="evaluation-fixture")


def evaluate_fixture(case: EvaluationCase, root: Path, output_dir: Path) -> dict[str, Any]:
    fixture_path = root / case.file
    slither_json_path = output_dir / f"{fixture_path.stem}.slither.json"
    raw = slither.run_slither(fixture_path, slither_json_path)
    findings = slither.parse_slither_results(raw)
    source_context.attach_source_context(findings, root)

    by_detector = {finding.detector: finding for finding in findings}
    if case.expected_clean:
        primary = [
            finding
            for finding in findings
            if finding.severity
            not in {Severity.INFORMATIONAL, Severity.OPTIMIZATION}
        ]
        if primary:
            actual = ", ".join(sorted(finding.detector for finding in primary))
            raise AssertionError(f"{case.name}: expected no primary findings, got {actual}")

    for detector in case.expected_detectors:
        if detector not in by_detector:
            raise AssertionError(f"{case.name}: expected detector {detector!r} was not produced")

    for detector, severity in case.expected_severities.items():
        actual = by_detector.get(detector)
        if actual is None:
            raise AssertionError(f"{case.name}: cannot check missing detector {detector!r}")
        if actual.severity != severity:
            raise AssertionError(
                f"{case.name}: detector {detector!r} severity {actual.severity.value!r}, "
                f"expected {severity.value!r}"
            )

    for finding in findings:
        finding.ai = build_grounded_evaluation_explanation(
            finding, case.expected_explanation_keywords
        )
        finding.ai_expanded = True

    sarif = report.generate_sarif(findings)
    if sarif["version"] != "2.1.0":
        raise AssertionError(f"{case.name}: SARIF version is not 2.1.0")

    return {
        "case": case.name,
        "file": case.file,
        "expected_detectors": case.expected_detectors,
        "actual_detectors": sorted(by_detector),
        "total_findings": len(findings),
        "sarif_results": len(sarif["runs"][0]["results"]),
        "grounded_explanations": sum(1 for finding in findings if finding.ai.ai_success),
    }
