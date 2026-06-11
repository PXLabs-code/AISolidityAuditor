# Real-project demo artifacts

Pinned Glamsterdam readiness demo outputs for grant review and reproducibility.

| Demo | Commit | Action run | Notes |
|------|--------|------------|-------|
| [transmissions11/solmate](transmissions11-solmate/89365b880c4f3c786bdd453d4b8e8fe410344a69/README.md) | `89365b880c4f3c786bdd453d4b8e8fe410344a69` | [run #27331627981](https://github.com/PXLabs-code/AISolidityAuditor/actions/runs/27331627981) | 5 Slither + 106 readiness (`src/`) |
| [OpenZeppelin/openzeppelin-contracts](openzeppelin-contracts/5fd1781b1454fd1ef8e722282f86f9293cacf256/README.md) | `5fd1781b1454fd1ef8e722282f86f9293cacf256` (`v5.6.1`) | [run #27342242106](https://github.com/PXLabs-code/AISolidityAuditor/actions/runs/27342242106) | 0 Slither + 609 readiness (`contracts/`) |

Refresh locally:

```bash
python scripts/run_real_project_demo.py --demo transmissions11-solmate
python scripts/run_real_project_demo.py --demo openzeppelin-contracts
```

Run the GitHub Actions demo workflow:

```bash
gh workflow run real-project-demo.yml -f demo=transmissions11-solmate
gh workflow run real-project-demo.yml -f demo=openzeppelin-contracts
```
