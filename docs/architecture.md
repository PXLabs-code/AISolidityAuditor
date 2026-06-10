# Architecture

## Overview

AISolidityAuditor is a monolithic app: Python FastAPI backend + React frontend. It invokes Slither via subprocess and calls an OpenAI-compatible API for AI explanations.

## Data flow

```
User uploads ZIP
  → Extract to /data/jobs/{taskId}/project/
  → Slither --json writes slither.json
  → Parse into findings.json (normalized)
  → AI explains each finding (up to 20)
  → Generate report.md
  → Frontend polls and displays results
```

## Components

| Component | Responsibility |
|-----------|----------------|
| `upload.py` | ZIP validation and safe extraction |
| `slither.py` | Slither CLI invocation and JSON parsing |
| `ai.py` | OpenAI-compatible API explanations |
| `report.py` | Markdown report generation |
| `audit.py` | Audit pipeline orchestration |
| `storage.py` | Filesystem task storage |
| `cleanup.py` | Expired job directory cleanup |

## API

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/audits` | Upload ZIP |
| GET | `/api/v1/audits/{taskId}` | Task status |
| GET | `/api/v1/audits/{taskId}/findings` | Findings list |
| GET | `/api/v1/audits/{taskId}/report` | Markdown report |
| GET | `/api/v1/audits/{taskId}/slither` | Raw Slither JSON |
| GET | `/api/health` | Health check |

## Deployment

- Development: backend `uvicorn` + frontend `vite dev` (proxies `/api`)
- Production: `docker compose up` single container; FastAPI serves built frontend static files

## Security

- ZIP path traversal protection
- Symbolic links rejected
- File size limit (10 MB)
- API keys not persisted or logged
- Upload rate limiting per IP (in-memory counter)

## Job cleanup

`cleanup.py` runs on application startup and hourly to delete task directories older than `JOB_RETENTION_HOURS` (default 24h).

## Known limitations

- Not a formal audit; AI explanations may be inaccurate
- Static analysis only; does not cover business-logic bugs
- Complex Foundry/Hardhat projects may require manual ZIP adjustments
