# Real-project demo: transmissions11/solmate

## Repository

- **Repo**: [transmissions11/solmate](https://github.com/transmissions11/solmate)
- **Commit SHA**: `89365b880c4f3c786bdd453d4b8e8fe410344a69`
- **Commit title**: Update LICENSE (2025-07-21)
- **Project path (Slither)**: `.` (Foundry root after `forge build`)
- **Project path (readiness heuristics)**: `src/`

## Action run

- **Workflow**: [.github/workflows/real-project-demo.yml](../../../.github/workflows/real-project-demo.yml)
- **Trigger**: `workflow_dispatch` with demo `transmissions11-solmate`
- **Workflow run**: run after merge via GitHub Actions; URL pattern:
  `https://github.com/PXLabs-code/AISolidityAuditor/actions/workflows/real-project-demo.yml`
- **Mode**: `glamsterdam-readiness`

Local generation command (readiness artifacts; full Slither requires Foundry + Slither):

```bash
python scripts/run_real_project_demo.py --demo transmissions11-solmate
```

## Results (readiness pass on `src/`)

| Detector | Count |
|----------|------:|
| `glamsterdam-gas-sensitive-loop` | 31 |
| `glamsterdam-low-level-evm` | 43 |
| `glamsterdam-eth-transfer-assumption` | 12 |
| `glamsterdam-block-context` | 17 |
| `glamsterdam-contract-size-watch` | 3 |
| **Total readiness findings** | **106** |

Slither triage counts are populated by the GitHub Actions workflow run (`audit-report.md`, `findings.json`, `slither.json`).

## Artifacts in this directory

| File | Contents |
|------|----------|
| `audit-report.md` | Slither triage report only |
| `findings.json` | Slither findings only |
| `slither.json` | Raw Slither JSON |
| `audit-results.sarif` | Merged SARIF with `tool` / `source` metadata |
| `glamsterdam-readiness-report.md` | Readiness heuristics only |
| `glamsterdam-findings.json` | Readiness findings only |
| `run-metadata.json` | Machine-readable demo metadata |

## Setup notes

- solmate is a Foundry project using `solc 0.8.15`.
- Run `forge build` before Slither on the repo root.
- Readiness heuristics intentionally scan `src/` to focus on library contracts rather than vendored `lib/` dependencies.
- `audit-report.md` and `findings.json` must not contain readiness heuristics.
- Readiness heuristics appear only in Glamsterdam artifacts and in SARIF rules tagged `readiness-heuristic`.
