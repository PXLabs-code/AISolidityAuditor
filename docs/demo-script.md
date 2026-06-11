# Demo recording script (~5 minutes)

## Preparation

1. `docker compose up --build`
2. Open http://localhost:8000 in a browser
3. Use the bundled `examples/reentrancy-example.zip` (no manual packaging needed)
4. Have an OpenAI API key ready, or configure another supported provider in `.env`

## Flow

1. **Introduction** (30s)
   - Show the home page: "Solidity Security Triage Assistant"
   - Explain: upload ZIP -> Slither -> assistive explanation -> report

2. **Upload** (30s)
   - Drag `reentrancy-example.zip`
   - Enter API key if needed
   - Click "Start Triage"

3. **Wait** (60-120s)
   - Show task page status: Running Slither -> AI explaining
   - Highlight that no CLI is required

4. **Results** (90s)
   - Show summary stats (High/Medium/etc.)
   - Switch to "Findings" tab; show assistive explanation for reentrancy
   - Switch to "Triage Report" tab; show Markdown report
   - Click "Download report"

5. **Closing** (30s)
   - Emphasize: open source, self-hostable, Ethereum ecosystem
   - Show GitHub Action, SARIF, and `docker compose up` deployment
   - Mention that every result remains manual-review required
