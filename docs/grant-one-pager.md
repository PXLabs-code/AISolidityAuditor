# Grant one-pager

## Problem

Slither is widely used in the Ethereum ecosystem, but its output targets security experts. Small teams struggle to understand findings and act on them, so vulnerabilities may still reach mainnet.

## Solution

**AISolidityAuditor** — an open-source, self-hostable web platform:

1. Upload a Solidity project ZIP
2. Run Slither automatically
3. AI translates each finding into readable English (problem, impact, fix)
4. Generate a Markdown security triage report automatically

## Impact

- Lowers the barrier to smart contract security self-checks
- Complements the official Slither ecosystem without reinventing analysis
- MIT licensed, Docker one-command deploy, no vendor lock-in

## Open source

- Public GitHub repository
- MIT License
- Full docs: architecture, threat model, known limitations
- Sample contracts and demo recording

## Roadmap (post-MVP)

1. GitHub Action for PR audits
2. Foundry/Hardhat template support
3. Multiple models / local LLM (Ollama)
4. Etherscan contract address import
