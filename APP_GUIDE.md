# Downloadable SOL paper bot

This package contains the updated Python bot, configuration, dashboard and tests.
API credentials, account databases, logs and the workspace's installed environment
are intentionally excluded. The package is for a computer or server running
Python 3.10 or later; a ZIP does not install a native iPhone or Android app.

The local dashboard is a browser interface. To use it from a phone, a separate
HTTPS deployment with access controls is still required. Alpaca paper trading
does not connect to Phantom or spend wallet funds. No live-money trading mode is
included in the Alpaca adapter.

## Mac / Linux

Unzip, open a terminal in `trading-bot`, then:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python configure_paper.py
.venv/bin/python -m trading_bot.main --check-alpaca
.venv/bin/python -m trading_bot.main --alpaca-paper
```

## Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -e '.[dev]'
.venv\Scripts\python.exe configure_paper.py
.venv\Scripts\python.exe -m trading_bot.main --check-alpaca
.venv\Scripts\python.exe -m trading_bot.main --alpaca-paper
```

The credential helper prompts with hidden input and writes the local `.env`.
Use a newly rotated pair after sharing credentials in chat. Do not share your
configured `.env` or repackage it with the app.

Open http://127.0.0.1:8000 on that same computer. Stop with Ctrl+C. Startup stops
if Alpaca has open positions or pending orders; reconcile those in your dedicated
paper account first. Stopping the bot does not close holdings.

Limits saved in `config/risk.yaml`: $1,000 allocation, $500 absolute entry cap,
5% maximum position exposure, one open position. The percentage rule initially
limits positions to $50. These are paper-testing limits, not profit or loss
guarantees. MockJev supplies test scores; the strategy has not demonstrated an
edge. See `ALPACA_SETUP.md` for execution behavior and limitations.
