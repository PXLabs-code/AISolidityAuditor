import shutil
from pathlib import Path

import pytest

from app.services import evaluation, slither


@pytest.mark.integration
def test_evaluation_fixtures_run_slither_generate_sarif_and_grounded_explanations(tmp_path):
    if not shutil.which("slither"):
        pytest.skip("slither executable is not available")
    if not shutil.which("solc"):
        pytest.skip("solc executable is not available")

    root = Path(__file__).resolve().parents[2] / "examples" / "evaluation"
    cases = evaluation.load_evaluation_manifest(root)
    assert len(cases) >= 30

    results = []
    for case in cases:
        results.append(evaluation.evaluate_fixture(case, root, tmp_path))

    assert all(result["sarif_results"] == result["total_findings"] for result in results)
    assert all(
        result["grounded_explanations"] == result["total_findings"] for result in results
    )


def test_evaluation_harness_uses_production_slither_parser(slither_raw):
    findings = slither.parse_slither_results(slither_raw)
    assert findings
