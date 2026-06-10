import json
import logging
from typing import Optional

import httpx

from app.config import settings
from app.models.schemas import AIExplanation, Finding

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a smart contract security audit assistant. Your task is to translate technical alerts from the Slither static analysis tool into clear explanations for developers.

Strict requirements:
1. Only explain based on the provided Slither finding; do not invent issues that were not reported
2. When uncertain, explicitly state "manual review required"
3. Write in English; technical terms (e.g. reentrancy) may remain as-is
4. Respond with valid JSON only; do not wrap in markdown code blocks"""

USER_PROMPT_TEMPLATE = """Explain the following Slither security finding:

Detector: {detector}
Severity: {severity}
Description: {description}
Contract: {contract}
Function: {function}
Location: {location}

Reply in JSON with these fields:
- title: short English title (max 50 characters)
- problem: what is wrong (developer-facing)
- impact: potential impact
- recommendation: concrete fix guidance"""


async def explain_finding(
    finding: Finding,
    api_key: str,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
) -> AIExplanation:
    key = api_key or settings.openai_api_key
    if not key:
        return AIExplanation(
            title=finding.detector,
            problem=finding.description,
            impact="No AI API key configured; explanation unavailable",
            recommendation="Configure an OpenAI-compatible API key and retry",
            ai_success=False,
        )

    location = ""
    if finding.file:
        location = finding.file
        if finding.line:
            location += f":{finding.line}"

    prompt = USER_PROMPT_TEMPLATE.format(
        detector=finding.detector,
        severity=finding.severity.value,
        description=finding.description,
        contract=finding.contract or "unknown",
        function=finding.function or "unknown",
        location=location or "unknown",
    )

    url = (base_url or settings.openai_base_url).rstrip("/") + "/chat/completions"
    model_name = model or settings.openai_model

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)

            return AIExplanation(
                title=parsed.get("title", finding.detector),
                problem=parsed.get("problem", finding.description),
                impact=parsed.get("impact", ""),
                recommendation=parsed.get("recommendation", ""),
                ai_success=True,
            )
    except Exception as exc:
        logger.warning("AI explanation failed for %s: %s", finding.id, exc)
        return AIExplanation(
            title=finding.detector,
            problem=finding.description,
            impact="AI explanation failed; showing original Slither description below",
            recommendation="Consult Slither documentation or a security expert",
            ai_success=False,
        )


async def explain_findings(
    findings: list[Finding],
    api_key: str,
    max_count: Optional[int] = None,
) -> list[Finding]:
    limit = max_count or settings.max_ai_findings
    result: list[Finding] = []

    for i, finding in enumerate(findings):
        if i < limit:
            ai = await explain_finding(finding, api_key)
            finding.ai = ai
            finding.ai_expanded = True
        else:
            finding.ai = AIExplanation(
                title=finding.detector,
                problem=finding.description,
                impact="",
                recommendation="",
                ai_success=False,
            )
            finding.ai_expanded = False

        result.append(finding)

    return result
