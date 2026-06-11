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
from app.models.schemas import AuditMeta, AuditStatus  # noqa: E402
from app.services import ai, report, slither, source_context  # noqa: E402


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


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

    slither_json_path = output_dir / "slither.json"
    raw = slither.run_slither(project, slither_json_path)
    _write_json(slither_json_path, raw)

    findings = slither.parse_slither_results(raw)
    source_context.attach_source_context(findings, project)
    provider_key = args.anthropic_api_key if args.ai_provider == "claude" else args.openai_api_key
    explained = await ai.explain_findings(findings, provider_key or "", provider_name=args.ai_provider)

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
    _write_json(output_dir / "audit-results.sarif", report.generate_sarif(explained))

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AISolidityAuditor in GitHub Actions")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ai-provider", choices=["openai", "claude"], default="openai")
    parser.add_argument("--openai-api-key", default="")
    parser.add_argument("--anthropic-api-key", default="")
    return parser.parse_args()


def main() -> None:
    asyncio.run(run_action_audit(parse_args()))


if __name__ == "__main__":
    main()
