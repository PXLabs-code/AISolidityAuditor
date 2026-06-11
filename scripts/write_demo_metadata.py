#!/usr/bin/env python3
"""Write README and run-metadata.json for a real-project demo output directory."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def write_metadata(
    output_dir: Path,
    *,
    demo_id: str,
    repo: str,
    commit: str,
    project_path: str,
    readiness_path: str,
    action_run_url: str,
) -> None:
    findings = json.loads((output_dir / "findings.json").read_text(encoding="utf-8"))
    readiness = json.loads((output_dir / "glamsterdam-findings.json").read_text(encoding="utf-8"))
    sarif = json.loads((output_dir / "audit-results.sarif").read_text(encoding="utf-8"))
    rules = sarif["runs"][0]["tool"]["driver"]["rules"]
    glamsterdam_rules = [rule for rule in rules if rule["id"].startswith("glamsterdam-")]

    readiness_by_detector: dict[str, int] = {}
    for item in readiness:
        detector = item["detector"]
        readiness_by_detector[detector] = readiness_by_detector.get(detector, 0) + 1

    generated_at = datetime.now(timezone.utc).isoformat()
    metadata = {
        "demo_id": demo_id,
        "repo": repo,
        "commit": commit,
        "project_path_slither": project_path,
        "project_path_readiness": readiness_path,
        "mode": "glamsterdam-readiness",
        "action_workflow": ".github/workflows/real-project-demo.yml",
        "action_run_url": action_run_url,
        "generated_at": generated_at,
        "slither_findings_total": len(findings),
        "readiness_findings_total": len(readiness),
        "readiness_findings_by_detector": readiness_by_detector,
        "glamsterdam_sarif_rules": len(glamsterdam_rules),
    }
    (output_dir / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    readme_lines = [
        "# Real-project demo: transmissions11/solmate",
        "",
        "## Repository",
        "",
        f"- **Repo**: `{repo}`",
        f"- **Commit SHA**: `{commit}`",
        f"- **Project path (Slither)**: `{project_path}`",
        f"- **Project path (readiness heuristics)**: `{readiness_path}`",
        "",
        "## Action run",
        "",
        f"- **Workflow run**: {action_run_url}",
        "- **Mode**: `glamsterdam-readiness`",
        f"- **Generated at**: {generated_at}",
        "",
        "## Results",
        "",
        f"- **Slither findings (reported)**: {len(findings)}",
        f"- **Glamsterdam readiness findings**: {len(readiness)}",
        f"- **Glamsterdam SARIF rules**: {len(glamsterdam_rules)}",
        "",
        "## Artifacts",
        "",
        "- `audit-report.md`",
        "- `findings.json`",
        "- `slither.json`",
        "- `audit-results.sarif`",
        "- `glamsterdam-readiness-report.md`",
        "- `glamsterdam-findings.json`",
        "- `run-metadata.json`",
        "",
    ]
    (output_dir / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write real-project demo metadata")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--demo-id", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--project-path", default=".")
    parser.add_argument("--readiness-path", default="src")
    parser.add_argument("--action-run-url", default=os.getenv("GITHUB_ACTION_RUN_URL", ""))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_metadata(
        args.output_dir,
        demo_id=args.demo_id,
        repo=args.repo,
        commit=args.commit,
        project_path=args.project_path,
        readiness_path=args.readiness_path,
        action_run_url=args.action_run_url,
    )


if __name__ == "__main__":
    main()
