#!/usr/bin/env python3
"""Run a pinned real-project Glamsterdam readiness demo and write artifacts."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.services import glamsterdam, report, slither  # noqa: E402
from app.services.report import build_summary  # noqa: E402

DEFAULT_DEMOS = {
    "transmissions11-solmate": {
        "repo": "https://github.com/transmissions11/solmate.git",
        "commit": "89365b880c4f3c786bdd453d4b8e8fe410344a69",
        "project_subpath": ".",
        "readiness_subpath": "src",
        "title": "transmissions11/solmate",
        "notes": "Foundry project. Slither runs on repo root after `forge build`; readiness heuristics scan `src/` only.",
    },
    "openzeppelin-contracts": {
        "repo": "https://github.com/OpenZeppelin/openzeppelin-contracts.git",
        "commit": "5fd1781b1454fd1ef8e722282f86f9293cacf256",
        "project_subpath": ".",
        "readiness_subpath": "contracts",
        "title": "OpenZeppelin/openzeppelin-contracts",
        "notes": (
            "Foundry project (v5.6.1 tag). Slither runs on repo root after `forge build`; "
            "readiness heuristics scan `contracts/` only (excludes test/mocks in other trees)."
        ),
    },
}


def _run(command: list[str], cwd: Path) -> None:
    result = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise RuntimeError(message or f"Command failed: {' '.join(command)}")


def _clone_repo(repo_url: str, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    _run(["git", "clone", "--depth", "1", repo_url, str(destination)], ROOT)


def _checkout_commit(repo_dir: Path, commit: str) -> None:
    _run(["git", "fetch", "--depth", "1", "origin", commit], repo_dir)
    _run(["git", "checkout", commit], repo_dir)


def _maybe_forge_build(project_dir: Path) -> str | None:
    forge = shutil.which("forge")
    if not forge:
        return None
    _run([forge, "build"], project_dir)
    return forge


def _tool_versions() -> dict[str, str | None]:
    slither_ok, slither_version = slither.check_slither_available()
    solc_ok = slither.check_solc_available()
    solc_version = None
    if solc_ok:
        result = subprocess.run(
            ["solc", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        solc_version = (result.stdout or result.stderr).strip().split("\n")[0]
    return {
        "slither": slither_version if slither_ok else None,
        "solc": solc_version,
        "forge": shutil.which("forge"),
    }


def _write_summary(
    output_dir: Path,
    demo_id: str,
    config: dict[str, str],
    versions: dict[str, str | None],
    slither_summary: dict | None,
    readiness_count: int,
    action_run_url: str | None,
) -> None:
    title = config.get("title", demo_id)
    readiness_subpath = config.get("readiness_subpath", config["project_subpath"])
    lines = [
        f"# Real-project demo: {title}",
        "",
        "## Repository",
        "",
        f"- **Repo**: `{config['repo']}`",
        f"- **Commit SHA**: `{config['commit']}`",
        f"- **Project path (Slither)**: `{config['project_subpath']}`",
        f"- **Project path (readiness heuristics)**: `{readiness_subpath}`",
        f"- **Demo ID**: `{demo_id}`",
        "",
        "## Action run",
        "",
    ]
    if action_run_url:
        lines.append(f"- **Workflow run**: {action_run_url}")
    else:
        lines.append(
            "- **Workflow run**: trigger `.github/workflows/real-project-demo.yml` "
            f"with `demo={demo_id}` to populate the GitHub Actions URL."
        )
    lines.extend(
        [
            "- **Mode**: `glamsterdam-readiness`",
            f"- **Generated at**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            "## Tooling",
            "",
            f"- **Slither**: `{versions.get('slither') or 'unavailable'}`",
            f"- **solc**: `{versions.get('solc') or 'unavailable'}`",
            f"- **forge**: `{versions.get('forge') or 'unavailable'}`",
            "",
            "## Results",
            "",
        ]
    )
    if slither_summary:
        lines.extend(
            [
                f"- **Slither findings (High/Medium/Low)**: "
                f"{slither_summary['high']}/{slither_summary['medium']}/{slither_summary['low']}",
                f"- **Slither findings (total)**: {slither_summary['total']}",
            ]
        )
    else:
        lines.append("- **Slither findings**: unavailable in this environment (readiness artifacts still generated).")
    lines.extend(
        [
            f"- **Glamsterdam readiness findings**: {readiness_count}",
            "",
            "## Artifacts",
            "",
            "- `audit-report.md` — Slither triage report only",
            "- `findings.json` — Slither findings only",
            "- `slither.json` — raw Slither JSON",
            "- `audit-results.sarif` — merged SARIF with tool/source metadata",
            "- `glamsterdam-readiness-report.md` — readiness heuristics only",
            "- `glamsterdam-findings.json` — readiness findings only",
            "",
            "## Setup notes",
            "",
            f"- {config['notes']}",
            "- `audit-report.md` and `findings.json` must not contain readiness heuristics.",
            "- Readiness heuristics appear only in Glamsterdam artifacts and tagged SARIF rules.",
            "",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def run_demo(
    demo_id: str,
    work_dir: Path,
    output_dir: Path,
    action_run_url: str | None = None,
) -> None:
    config = DEFAULT_DEMOS[demo_id]
    repo_dir = work_dir / demo_id
    project_dir = repo_dir / config["project_subpath"]
    readiness_dir = repo_dir / config.get("readiness_subpath", config["project_subpath"])

    _clone_repo(config["repo"], repo_dir)
    _checkout_commit(repo_dir, config["commit"])
    forge = _maybe_forge_build(project_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    versions = _tool_versions()

    slither_summary = None
    slither_findings = []
    raw: dict = {"results": {"detectors": []}}
    slither_json_path = output_dir / "slither.json"

    if versions["slither"]:
        raw = slither.run_slither(project_dir, slither_json_path)
        slither_json_path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        slither_findings = slither.parse_slither_results(raw)
        primary = [
            finding
            for finding in slither_findings
            if finding.severity.value not in {"Informational", "Optimization"}
        ]
        summary = build_summary(primary)
        slither_summary = summary.model_dump()
        findings_json = [finding.model_dump(mode="json") for finding in primary]
        (output_dir / "findings.json").write_text(
            json.dumps(findings_json, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        from app.models.schemas import AuditMeta, AuditStatus  # noqa: E402

        meta = AuditMeta(
            task_id=f"real-project-demo-{demo_id}",
            status=AuditStatus.COMPLETED,
            filename=project_dir.name,
            created_at="",
            updated_at="",
            summary=summary,
            duration_sec=0.0,
        )
        slither_version = versions["slither"] or "unknown"
        (output_dir / "audit-report.md").write_text(
            report.generate_report(meta, primary, slither_version=slither_version),
            encoding="utf-8",
        )
    else:
        slither_json_path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        (output_dir / "findings.json").write_text("[]\n", encoding="utf-8")
        (output_dir / "audit-report.md").write_text(
            "# Solidity Security Triage Report\n\n*Slither was unavailable in this environment.*\n",
            encoding="utf-8",
        )

    readiness_findings = glamsterdam.scan_project(readiness_dir)
    (output_dir / "glamsterdam-findings.json").write_text(
        json.dumps(
            [finding.model_dump(mode="json") for finding in readiness_findings],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (output_dir / "glamsterdam-readiness-report.md").write_text(
        glamsterdam.generate_readiness_report(project_dir.name, readiness_findings),
        encoding="utf-8",
    )

    sarif_tags = [
        "glamsterdam",
        "gas-repricing",
        "evm-compatibility",
        "eth-transfer-logs",
        "contract-size",
    ]
    sarif_findings = [*slither_findings, *readiness_findings]
    (output_dir / "audit-results.sarif").write_text(
        json.dumps(
            report.generate_sarif(sarif_findings, readiness_tags=sarif_tags),
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    metadata = {
        "demo_id": demo_id,
        "repo": config["repo"],
        "commit": config["commit"],
        "project_path": config["project_subpath"],
        "mode": "glamsterdam-readiness",
        "action_run_url": action_run_url,
        "tooling": versions,
        "forge_build": forge is not None,
        "slither_summary": slither_summary,
        "readiness_count": len(readiness_findings),
    }
    (output_dir / "run-metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _write_summary(
        output_dir,
        demo_id,
        config,
        versions,
        slither_summary,
        len(readiness_findings),
        action_run_url,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a pinned real-project demo")
    parser.add_argument(
        "--demo",
        choices=sorted(DEFAULT_DEMOS),
        default="transmissions11-solmate",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=ROOT / ".cache" / "real-project-demos",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Defaults to docs/demo-artifacts/<demo>/<commit>/",
    )
    parser.add_argument("--action-run-url", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = DEFAULT_DEMOS[args.demo]
    output_dir = args.output_dir or (
        ROOT / "docs" / "demo-artifacts" / args.demo / config["commit"]
    )
    run_demo(
        args.demo,
        args.work_dir,
        output_dir,
        action_run_url=args.action_run_url or None,
    )
    print(f"Wrote demo artifacts to {output_dir}")


if __name__ == "__main__":
    main()
