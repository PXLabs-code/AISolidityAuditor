# Demo recording script (~5 minutes)

## Preparation

1. `docker compose up --build`
2. Open http://localhost:8000 in a browser
3. Use the bundled `examples/reentrancy-example.zip` (no manual packaging needed)
4. Have an OpenAI API key ready (or configure it in `.env`)

## Flow

1. **Introduction** (30s)
   - Show the home page: "AI Smart Contract Audit"
   - Explain: upload ZIP → Slither → AI explanation → report

2. **Upload** (30s)
   - Drag `reentrancy-example.zip`
   - Enter API key if needed
   - Click "Start Audit"

3. **Wait** (60–120s)
   - Show task page status: Running Slither → AI explaining
   - Highlight that no CLI is required

4. **Results** (90s)
   - Show summary stats (High/Medium/etc.)
   - Switch to "Findings" tab; show AI explanation for reentrancy
   - Switch to "Audit Report" tab; show Markdown report
   - Click "Download report"

5. **Closing** (30s)
   - Emphasize: open source, self-hostable, Ethereum ecosystem
   - Show GitHub repo and `docker compose up` one-command deploy
