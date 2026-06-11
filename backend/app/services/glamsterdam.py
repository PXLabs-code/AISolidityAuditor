from dataclasses import dataclass
from pathlib import Path

from app.models.schemas import Finding, Severity


@dataclass(frozen=True)
class ReadinessRule:
    detector: str
    severity: Severity
    title: str
    keywords: tuple[str, ...]
    recommendation: str


RULES = [
    ReadinessRule(
        detector="glamsterdam-eth-transfer-assumption",
        severity=Severity.LOW,
        title="Native ETH transfer assumption",
        keywords=(".transfer(", ".send(", ".call{value:", ".call.value("),
        recommendation=(
            "Review ETH transfer assumptions against proposed native ETH transfer logs "
            "and any gas repricing that may affect transfer-style patterns."
        ),
    ),
    ReadinessRule(
        detector="glamsterdam-gas-sensitive-loop",
        severity=Severity.INFORMATIONAL,
        title="Gas-sensitive loop",
        keywords=("for (", "for(", "while (", "while("),
        recommendation=(
            "Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals."
        ),
    ),
    ReadinessRule(
        detector="glamsterdam-low-level-evm",
        severity=Severity.INFORMATIONAL,
        title="Low-level EVM usage",
        keywords=("assembly", ".delegatecall(", ".staticcall(", ".call("),
        recommendation=(
            "Review low-level EVM assumptions against proposed opcode and EVM behavior changes."
        ),
    ),
    ReadinessRule(
        detector="glamsterdam-block-context",
        severity=Severity.INFORMATIONAL,
        title="Block context dependency",
        keywords=("block.timestamp", "block.number", "block.prevrandao", "block.coinbase"),
        recommendation=(
            "Review block context assumptions as Glamsterdam candidates include protocol-level "
            "changes such as ePBS and Block-Level Access Lists."
        ),
    ),
]


def _solidity_files(project_path: Path) -> list[Path]:
    if project_path.is_file() and project_path.suffix == ".sol":
        return [project_path]
    if project_path.is_dir():
        return sorted(project_path.rglob("*.sol"))
    return []


def _relative(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve())).replace("\\", "/")
    except ValueError:
        return path.name


def _code_portion(line: str) -> str:
    """Return executable code on a line, stripping // comments and string literals."""
    result: list[str] = []
    i = 0
    in_string = False
    string_char = ""
    while i < len(line):
        ch = line[i]
        if not in_string:
            if ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                break
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
                i += 1
                continue
            result.append(ch)
        else:
            if ch == "\\" and i + 1 < len(line):
                i += 2
                continue
            if ch == string_char:
                in_string = False
            i += 1
            continue
        i += 1
    return "".join(result)


def _source_context(lines: list[str], line_number: int) -> tuple[str, int, int]:
    start = max(1, line_number - 2)
    end = min(len(lines), line_number + 2)
    snippet = "\n".join(f"{idx}: {lines[idx - 1]}" for idx in range(start, end + 1))
    return snippet, start, end


def scan_project(project_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    base = project_path if project_path.is_dir() else project_path.parent
    seen: set[tuple[str, str, int]] = set()

    for file_path in _solidity_files(project_path):
        if not file_path.is_file():
            continue
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        rel = _relative(file_path, base)
        if len(file_path.read_text(encoding="utf-8", errors="replace")) > 20_000:
            key = ("glamsterdam-contract-size-watch", rel, 1)
            if key not in seen:
                seen.add(key)
                findings.append(
                    Finding(
                        id=f"glamsterdam-{len(findings) + 1}",
                        detector="glamsterdam-contract-size-watch",
                        severity=Severity.INFORMATIONAL,
                        description=(
                            "Large Solidity source file. Review contract-size assumptions "
                            "against Glamsterdam max contract size discussions."
                        ),
                        file=rel,
                        line=1,
                        source="readiness-heuristic",
                    )
                )

        for line_number, line in enumerate(lines, start=1):
            code = _code_portion(line)
            if not code.strip():
                continue
            compact = code.replace(" ", "")
            for rule in RULES:
                haystacks = (code, compact)
                if not any(keyword in haystack for keyword in rule.keywords for haystack in haystacks):
                    continue
                key = (rule.detector, rel, line_number)
                if key in seen:
                    continue
                seen.add(key)
                snippet, start, end = _source_context(lines, line_number)
                findings.append(
                    Finding(
                        id=f"glamsterdam-{len(findings) + 1}",
                        detector=rule.detector,
                        severity=rule.severity,
                        description=f"{rule.title}. {rule.recommendation}",
                        file=rel,
                        line=line_number,
                        source_context=snippet,
                        source_start_line=start,
                        source_end_line=end,
                        source="readiness-heuristic",
                    )
                )

    return findings


def _readiness_findings(findings: list[Finding]) -> list[Finding]:
    return [finding for finding in findings if finding.source == "readiness-heuristic"]


def generate_readiness_report(project_name: str, findings: list[Finding]) -> str:
    findings = _readiness_findings(findings)
    lines = [
        "# Glamsterdam Solidity Readiness Report",
        "",
        f"- **Project**: {project_name}",
        f"- **Readiness findings**: {len(findings)}",
        "",
        "> This report contains Glamsterdam readiness heuristics only. Slither findings are "
        "published separately in `audit-report.md` and `findings.json`.",
        "",
        "> This report is an early readiness triage for proposed Glamsterdam-related changes. "
        "It is not a protocol compatibility guarantee and requires manual review.",
        "",
        "## Focus Areas",
        "",
        "- Gas repricing and gas-sensitive source patterns",
        "- EVM opcode or low-level call assumptions",
        "- Native ETH transfer logging assumptions",
        "- Block context assumptions around ePBS and Block-Level Access Lists",
        "- Contract-size watch points",
        "",
        "## Findings",
        "",
    ]

    if not findings:
        lines.append("*No Glamsterdam readiness patterns were detected by the current heuristics.*")
    else:
        for finding in findings:
            location = finding.file or "unknown"
            if finding.line:
                location = f"{location}:{finding.line}"
            lines.extend(
                [
                    f"### [{finding.severity.value}] {finding.detector}",
                    "",
                    f"- **Location**: `{location}`",
                    f"- **Review note**: {finding.description}",
                    "- **Manual review required**: Yes",
                    "",
                ]
            )
            if finding.source_context:
                lines.extend(["```solidity", finding.source_context, "```", ""])

    lines.extend(
        [
            "## Limitations",
            "",
            "- Glamsterdam EIPs are still under consideration and may change.",
            "- Readiness heuristics are separate from Slither static-analysis evidence.",
            "- Findings are review prompts, not vulnerability claims.",
        ]
    )
    return "\n".join(lines)
