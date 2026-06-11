# Real-project demo: OpenZeppelin/openzeppelin-contracts

## Repository

- **Repo**: `https://github.com/OpenZeppelin/openzeppelin-contracts`
- **Commit SHA**: `5fd1781b1454fd1ef8e722282f86f9293cacf256` (tag `v5.6.1`)
- **Project path (Slither)**: `.`
- **Project path (readiness heuristics)**: `contracts`

## Action run

- **Workflow run**: https://github.com/PXLabs-code/AISolidityAuditor/actions/runs/27342242106
- **Mode**: `glamsterdam-readiness`
- **Generated at**: 2026-06-11T11:03:41.974984+00:00

## Results

- **Slither findings (reported)**: 0
- **Glamsterdam readiness findings**: 609
- **Glamsterdam SARIF rules**: 5

## Slither summary (informational excluded)

| Severity | Count |
|----------|------:|
| High | 0 |
| Medium | 0 |
| Low | 0 |
| **Total reported** | **0** |

## Readiness summary (`contracts/`)

| Detector | Count |
|----------|------:|
| `glamsterdam-low-level-evm` | 449 |
| `glamsterdam-gas-sensitive-loop` | 104 |
| `glamsterdam-block-context` | 34 |
| `glamsterdam-contract-size-watch` | 12 |
| `glamsterdam-eth-transfer-assumption` | 10 |

## Artifacts

- `audit-report.md` — Slither triage only
- `findings.json` — Slither findings only
- `slither.json` — raw Slither JSON
- `audit-results.sarif` — merged SARIF with tool/source metadata
- `glamsterdam-readiness-report.md` — readiness heuristics only
- `glamsterdam-findings.json` — readiness findings only
- `run-metadata.json` — machine-readable metadata

## Setup notes

- OpenZeppelin Contracts v5.6.1 is a Foundry project (`solc 0.8.27` in `foundry.toml`).
- Workflow runs `forge build` before Slither on the repo root.
- Readiness heuristics scan `contracts/` only (library sources, not `test/`).
- `include_informational: false` in the demo workflow, so informational Slither findings are omitted from `findings.json` and `audit-report.md`.
- Zero reported Slither High/Medium/Low findings on this pin is expected for a mature audited library; readiness counts are high-recall review prompts, mostly low-confidence `low-level-evm` and `gas-sensitive-loop` rules.
