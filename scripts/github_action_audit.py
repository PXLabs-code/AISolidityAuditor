import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

ACTION_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ACTION_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings  # noqa: E402
from app.models.schemas import AuditMeta, AuditStatus, Severity  # noqa: E402
from app.services import ai, glamsterdam, report, slither, source_context  # noqa: E402


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _filter_findings(findings, include_informational: bool):
    if include_informational:
        return findings
    return [
        finding
        for finding in findings
        if finding.severity not in {Severity.INFORMATIONAL, Severity.OPTIMIZATION}
    ]


async def run_action_audit(args: argparse.Namespace) -> None:
    start = time.time()
    project = args.project.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    settings.ai_provider = args.ai_provider
    if args.openai_api_key:
        settings.openai_api_key = args.openai_api_key
    if args.anthropic_api_key:
        settings.anthropic_api_key = args.anthropic_api_key
    if args.deepseek_api_key:
        settings.deepseek_api_key = args.deepseek_api_key

    slither_json_path = output_dir / "slither.json"
    raw = slither.run_slither(project, slither_json_path)
    _write_json(slither_json_path, raw)

    findings = slither.parse_slither_results(raw)
    source_context.attach_source_context(findings, project)
    findings = _filter_findings(findings, _parse_bool(args.include_informational))
    readiness_findings = []
    if args.mode == "glamsterdam-readiness":
        readiness_root = args.readiness_project.resolve() if args.readiness_project else project
        readiness_findings = glamsterdam.scan_project(readiness_root)
        _write_json(
            output_dir / "glamsterdam-findings.json",
            [finding.model_dump(mode="json") for finding in readiness_findings],
        )
        readiness_report = glamsterdam.generate_readiness_report(
            project.name,
            readiness_findings,
        )
        (output_dir / "glamsterdam-readiness-report.md").write_text(
            readiness_report,
            encoding="utf-8",
        )

    provider_key = {
        "claude": args.anthropic_api_key,
        "deepseek": args.deepseek_api_key,
        "openai": args.openai_api_key,
    }[args.ai_provider]
    explained = await ai.explain_findings(
        findings,
        provider_key or "",
        max_count=args.max_ai_findings,
        provider_name=args.ai_provider,
    )

    findings_json = [finding.model_dump(mode="json") for finding in explained]
    _write_json(output_dir / "findings.json", findings_json)

    summary = report.build_summary(explained)
    meta = AuditMeta(
        task_id=os.getenv("GITHUB_RUN_ID", "github-action"),
        status=AuditStatus.COMPLETED,
        filename=project.name,
        created_at="",
        updated_at="",
        summary=summary,
        duration_sec=round(time.time() - start, 1),
    )
    report_md = report.generate_report(meta, explained, slither_version="github-action")
    (output_dir / "audit-report.md").write_text(report_md, encoding="utf-8")
    sarif_tags: list[str] = []
    sarif_findings = explained
    if args.mode == "glamsterdam-readiness":
        sarif_tags = [
            "glamsterdam",
            "gas-repricing",
            "evm-compatibility",
            "eth-transfer-logs",
            "contract-size",
        ]
        sarif_findings = [*explained, *readiness_findings]
    _write_json(
        output_dir / "audit-results.sarif",
        report.generate_sarif(sarif_findings, readiness_tags=sarif_tags),
    )

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write("## AISolidityAuditor\n\n")
            fh.write(f"- Total findings: {summary.total}\n")
            fh.write(f"- High: {summary.high}\n")
            fh.write(f"- Medium: {summary.medium}\n")
            fh.write(f"- Low: {summary.low}\n")
            fh.write(f"- AI explained: {summary.ai_explained}\n")
            fh.write(f"- Report: `{output_dir / 'audit-report.md'}`\n")
            if args.mode == "glamsterdam-readiness":
                fh.write(f"- Glamsterdam readiness findings: {len(readiness_findings)}\n")
                fh.write(
                    f"- Glamsterdam report: `{output_dir / 'glamsterdam-readiness-report.md'}`\n"
                )

    if _parse_bool(args.fail_on_high) and summary.high:
        raise SystemExit(f"AISolidityAuditor found {summary.high} High finding(s)")
    if _parse_bool(args.fail_on_medium) and summary.medium:
        raise SystemExit(f"AISolidityAuditor found {summary.medium} Medium finding(s)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AISolidityAuditor in GitHub Actions")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument(
        "--readiness-project",
        type=Path,
        default=None,
        help="Optional path for Glamsterdam readiness heuristics (defaults to --project).",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ai-provider", choices=["openai", "claude", "deepseek"], default="openai")
    parser.add_argument(
        "--mode",
        choices=["standard", "glamsterdam-readiness"],
        default="standard",
    )
    parser.add_argument("--openai-api-key", default="")
    parser.add_argument("--anthropic-api-key", default="")
    parser.add_argument("--deepseek-api-key", default="")
    parser.add_argument("--max-ai-findings", type=int, default=20)
    parser.add_argument("--include-informational", default="true")
    parser.add_argument("--fail-on-high", default="false")
    parser.add_argument("--fail-on-medium", default="false")
    return parser.parse_args()


def main() -> None:
    asyncio.run(run_action_audit(parse_args()))


if __name__ == "__main__":
    main()
