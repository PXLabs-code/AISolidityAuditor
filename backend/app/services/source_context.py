from pathlib import Path

from app.models.schemas import Finding

MAX_CONTEXT_LINES = 80
WINDOW_RADIUS = 18


def _safe_source_path(project_path: Path, file_name: str) -> Path | None:
    base = project_path.resolve()
    candidates = [base / file_name]
    candidates.extend(base.rglob(Path(file_name).name))

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            resolved.relative_to(base)
        except (FileNotFoundError, ValueError):
            continue
        if resolved.is_file():
            return resolved
    return None


def _brace_delta(line: str) -> int:
    stripped = line.split("//", 1)[0]
    return stripped.count("{") - stripped.count("}")


def _extract_block(lines: list[str], line_number: int) -> tuple[int, int]:
    index = max(0, min(line_number - 1, len(lines) - 1))
    start = max(0, index - WINDOW_RADIUS)
    end = min(len(lines) - 1, index + WINDOW_RADIUS)

    for cursor in range(index, max(-1, index - WINDOW_RADIUS - 1), -1):
        stripped = lines[cursor].strip()
        if (
            stripped.startswith("function ")
            or stripped.startswith("constructor")
            or stripped.startswith("modifier ")
            or stripped.startswith("fallback")
            or stripped.startswith("receive")
        ):
            start = cursor
            break

    depth = 0
    seen_open = False
    for cursor in range(start, min(len(lines), start + MAX_CONTEXT_LINES)):
        delta = _brace_delta(lines[cursor])
        if "{" in lines[cursor]:
            seen_open = True
        depth += delta
        if seen_open and depth <= 0 and cursor > start:
            end = cursor
            break

    if end < index:
        end = min(len(lines) - 1, index + WINDOW_RADIUS)

    if end - start + 1 > MAX_CONTEXT_LINES:
        end = start + MAX_CONTEXT_LINES - 1

    return start + 1, end + 1


def attach_source_context(findings: list[Finding], project_path: Path) -> list[Finding]:
    for finding in findings:
        if not finding.file or not finding.line:
            continue

        source_path = _safe_source_path(project_path, finding.file)
        if source_path is None:
            continue

        lines = source_path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not lines:
            continue

        start, end = _extract_block(lines, finding.line)
        snippet_lines = [
            f"{line_no}: {lines[line_no - 1]}" for line_no in range(start, end + 1)
        ]
        finding.source_context = "\n".join(snippet_lines)
        finding.source_start_line = start
        finding.source_end_line = end

    return findings
