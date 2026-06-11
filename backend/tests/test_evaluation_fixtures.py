import json
from pathlib import Path


def test_evaluation_fixture_manifest():
    root = Path(__file__).resolve().parents[2] / "examples" / "evaluation"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

    assert len(manifest) >= 30
    for item in manifest:
        assert (root / item["file"]).exists()
        assert "expected_detectors" in item
        assert "expected_severities" in item
        for detector in item["expected_detectors"]:
            assert detector in item["expected_severities"]
        assert "expected_explanation_keywords" in item
        assert item["expected_explanation_keywords"]
        if item.get("expected_clean"):
            assert item["expected_detectors"] == []
