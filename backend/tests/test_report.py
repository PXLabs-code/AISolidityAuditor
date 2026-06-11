from app.models.schemas import AIExplanation, AuditMeta, AuditStatus, Finding, Severity
from app.services.report import build_summary, generate_report, generate_sarif


def _finding_with_ai() -> Finding:
    return Finding(
        id="finding-1",
        detector="reentrancy-eth",
        severity=Severity.HIGH,
        description="Reentrancy in withdraw",
        contract="VulnerableBank",
        function="withdraw",
        file="Reentrancy.sol",
        line=15,
        source_context="15: function withdraw() external { msg.sender.call(\"\"); }",
        source_start_line=15,
        source_end_line=15,
        ai=AIExplanation(
            title="Reentrancy risk",
            problem="External call before state update",
            impact="Funds may be drained repeatedly",
            recommendation="Update state before external transfer",
            ai_success=True,
            confidence="high",
        ),
    )


def test_build_summary():
    summary = build_summary([_finding_with_ai()])
    assert summary.total == 1
    assert summary.high == 1
    assert summary.ai_explained == 1


def test_generate_report():
    meta = AuditMeta(
        task_id="test-task-id",
        status=AuditStatus.COMPLETED,
        filename="reentrancy-example.zip",
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
        duration_sec=12.5,
    )
    report = generate_report(meta, [_finding_with_ai()], slither_version="0.10.4")

    assert "# Solidity Security Triage Report" in report
    assert "reentrancy-example.zip" in report
    assert "Reentrancy risk" in report
    assert "reentrancy-eth" in report
    assert "Top risks" in report
    assert "Slither finding" in report
    assert "AI explanation" in report
    assert "Source context" in report
    assert "function withdraw" in report
    assert "AI confidence" in report
    assert "Manual review required" in report
    assert "Disclaimer" in report
    assert "/api/v1/audits/" in report
    assert "/slither" in report


def test_generate_report_empty_findings():
    meta = AuditMeta(
        task_id="empty-task",
        status=AuditStatus.COMPLETED,
        filename="clean.zip",
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
    )
    report = generate_report(meta, [])
    assert "No security issues detected" in report


def test_generate_report_ai_failure_reason():
    finding = Finding(
        id="finding-1",
        detector="reentrancy-eth",
        severity=Severity.HIGH,
        description="Reentrancy in withdraw",
        ai=AIExplanation(
            title="reentrancy-eth",
            problem="Reentrancy in withdraw",
            impact="AI explanation unavailable because no API key is configured",
            recommendation="Set the provider API key or pass one with the audit request",
            ai_success=False,
            provider="openai",
            error="No API key configured for openai",
        ),
    )
    meta = AuditMeta(
        task_id="failed-ai-task",
        status=AuditStatus.COMPLETED,
        filename="reentrancy-example.zip",
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
    )

    report = generate_report(meta, [finding])

    assert "| AI explained | 0 |" in report
    assert "AI explanation**: Unavailable (No API key configured for openai)" in report


def test_generate_report_sanitizes_multiline_ai_error():
    finding = Finding(
        id="finding-1",
        detector="reentrancy-eth",
        severity=Severity.HIGH,
        description="Reentrancy in withdraw",
        ai=AIExplanation(
            title="reentrancy-eth",
            problem="Reentrancy in withdraw",
            impact="AI failed",
            recommendation="Retry later",
            ai_success=False,
            provider="openai",
            error=(
                "Client error '429 Too Many Requests' for url 'https://api.openai.com/v1/chat/completions'\n"
                "For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
            ),
        ),
    )
    meta = AuditMeta(
        task_id="rate-limit-task",
        status=AuditStatus.COMPLETED,
        filename="reentrancy-example.zip",
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
    )

    report = generate_report(meta, [finding])

    assert "Client error '429 Too Many Requests'" in report
    assert ")\nFor more information" not in report


def test_generate_report_folds_informational_and_optimization_findings():
    finding = Finding(
        id="finding-1",
        detector="naming-convention",
        severity=Severity.INFORMATIONAL,
        description="Informational issue",
    )
    meta = AuditMeta(
        task_id="info-task",
        status=AuditStatus.COMPLETED,
        filename="info.zip",
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
    )

    report = generate_report(meta, [finding])

    assert "<details>" in report
    assert "Informational and Optimization findings" in report


def test_generate_sarif():
    sarif = generate_sarif([_finding_with_ai()])

    assert sarif["version"] == "2.1.0"
    run = sarif["runs"][0]
    assert run["tool"]["driver"]["name"] == "AISolidityAuditor"
    assert run["results"][0]["ruleId"] == "reentrancy-eth"
    assert run["results"][0]["level"] == "error"
