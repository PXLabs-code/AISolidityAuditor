import json
from pathlib import Path


def test_evaluation_fixture_manifest():
    root = Path(__file__).resolve().parents[2] / "examples" / "evaluation"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

    assert len(manifest) == 10
    for item in manifest:
        assert (root / item["file"]).exists()
        assert "expected_detectors" in item
        assert "expected_explanation_keywords" in item
        assert item["expected_explanation_keywords"]
