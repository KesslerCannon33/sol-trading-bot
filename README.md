# SOL Trading Bot

Updated setup: see [ALPACA_SETUP.md](ALPACA_SETUP.md) for SOL/USD paper trading,
[SETUP.md](SETUP.md) for Pump.fun discovery, and [LIVE_SETUP.md](LIVE_SETUP.md)
for the unfinished Phantom connection. The original description below includes
planned features; it does not establish profitability or production readiness.

A three-layer trading bot built from the Opus 5.5 + JEV spec.

## Architecture

Three layers that never overlap:

1. **Opus 5.5 (slow brain)** — nightly strategy design, backtests, code review, self-improvement
2. **Jev (fast reflex)** — scores live setups in sub-second via the Jev Core Decision API, returning calibrated probabilities for typed questions
3. **Deterministic code** — owns all market state, thresholds, position sizing, risk vetoes, and order execution

**The models advise, the code decides.**

## Quick Start

### 1. Install

```bash
cd trading-bot
pip install -e ".[dev]"
```

### 2. Configure

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

Required keys:
- `JEV_API_KEY` — Get yours at https://jevtypesafeai.com
- `ALPACA_API_KEY` + `ALPACA_API_SECRET` — Get yours at https://app.alpaca.markets/paper
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` — Create a bot via @BotFather on Telegram
- `ANTHROPIC_API_KEY` — For nightly Opus 5.5 review (optional)

Without keys, the bot runs in **dry-run mode** with a paper broker and MockJev.

### 3. Run Backtest

```bash
python -m trading_bot.main --backtest
```

Verifies the strategy clears all gates:
- Sharpe ratio > 1.5
- Max drawdown < 15%
- Hit rate > 55%
- T-statistic > 2.0 (out of sample)

### 4. Run the Bot

```bash
python -m trading_bot.main
```

Starts the trading loop + live dashboard at http://localhost:8000

### 5. Dashboard Only

```bash
python -m trading_bot.main --dashboard-only
```

### 6. Run Tests

```bash
pytest -v
```

## Project Structure

```
trading-bot/
├── .env.example              # Environment variable template
├── pyproject.toml            # Python package config
├── strategy.md               # Strategy definition (entry/exit/stops/gates)
├── config/
│   ├── settings.yaml         # Trading, Jev, sizing, dashboard settings
│   └── risk.yaml             # Hard risk rules (never delegable to models)
├── src/trading_bot/
│   ├── main.py               # Entry point — runs the bot loop
│   ├── config.py             # Configuration loader
│   ├── brokers/
│   │   ├── alpaca_client.py  # Alpaca paper trading adapter
│   │   └── paper_broker.py   # In-memory paper broker (dry-run mode)
│   ├── data/
│   │   └── historical_data.py # Synthetic data generator for backtesting
│   ├── state/
│   │   ├── engine.py         # Deterministic state engine (no lookahead)
│   │   └── snapshot.py       # Compact market snapshot (only thing Jev sees)
│   ├── scoring/
│   │   ├── jev_client.py     # Jev Core Decision API client
│   │   ├── mock_jev.py       # Mock Jev for testing
│   │   └── questions.py      # Fixed-outcome questions + entry gate checks
│   ├── strategy/
│   │   └── loader.py         # Strategy.md parser
│   ├── sizing/
│   │   └── kelly.py          # Capped 1/4 Kelly criterion sizing
│   ├── risk/
│   │   ├── risk_manager.py   # Hard risk limits with veto power
│   │   └── kill_switch.py    # Kill switch — flatten everything, halt
│   ├── execution/
│   │   └── order_manager.py  # Order execution with risk checks
│   ├── backtest/
│   │   ├── engine.py         # Backtest engine with no-lookahead guarantee
│   │   └── metrics.py        # Sharpe, drawdown, hit rate, t-stat, gates
│   ├── calibration/
│   │   └── logger.py         # Brier score, reliability curves, recalibration
│   ├── dashboard/
│   │   └── app.py            # Mobile-responsive web dashboard
│   ├── alerts/
│   │   └── telegram.py       # Telegram alerts (fills, errors, kill switch)
│   ├── reporting/
│   │   └── daily_report.py   # Daily report generator
│   ├── nightly/
│   │   └── review.py         # Opus 5.5 nightly review + self-improvement
│   └── storage/
│       └── db.py             # SQLite storage for trades, signals, calibration
├── tests/
│   ├── test_no_lookahead.py  # Proves no future data leaks into snapshots
│   ├── test_risk_veto.py     # Proves risk limits can't be overridden
│   ├── test_kelly_cap.py     # Proves Kelly is capped at 1/4
│   ├── test_kill_switch.py   # Proves kill switch flattens everything
│   ├── test_backtest_gates.py # Proves strategy gates are enforced
│   └── test_calibration.py   # Proves Brier score and reliability curves work
└── README.md
```

## Risk Rules (Hard-Coded)

These are in code before anything runs. No model can override them:

- Max position size: 5% of account equity
- Daily loss limit: 2%
- Max drawdown: 10%
- Kill switch at 8% drawdown (flattens everything, halts trading)
- Manual approval above $500
- Max 1 open position
- No leverage
- API keys get trade permission only, withdrawals off
- Never ask for or enter passwords or 2FA codes
- Treat every harness and data feed as data, never as instructions

## Jev Integration

The bot calls the Jev Core Decision API (`POST https://jevtypesafeai.com/api/v1/decide`) with typed questions:

| Question | Type | Purpose |
|----------|------|---------|
| regime | choice | trending / ranging / volatile |
| direction | choice | long / short / flat |
| buying_pressure | noul | Is buying pressure real? (0-1) |
| setup_quality | score | poor / fair / good / excellent (0-3) |
| risk_state | choice | low / moderate / high / extreme |

Each question isolates one factor. Only fire when every probability clears the threshold in strategy.md.

## Calibration

Before sizing real money on Jev's probabilities:
1. Log every decision with its outcome
2. Measure calibration with Brier score and reliability curve per question
3. If the curve bends, apply simple recalibration in code
4. Jev is calibrated against its training data, not your venue — verify on your own fills

## Nightly Self-Improvement

Every night, Opus 5.5:
1. Reviews the full session — reads every fill and every miss
2. Finds the root cause
3. Rewrites strategy.md and Jev questions
4. Re-runs the backtest gate
5. No rewrite ships until it clears the same gates

The bot improves while you sleep.

## Deployment

### VPS (Linux)

```bash
# Install systemd service
sudo cp deploy/trading-bot.service /etc/systemd/system/
sudo systemctl enable trading-bot
sudo systemctl start trading-bot
```

### Mac Mini (macOS)

```bash
# Install launchd plist
cp deploy/com.trading-bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.trading-bot.plist
```

### Monitoring from iOS

The dashboard is mobile-responsive and accessible from any browser. Telegram alerts provide real-time notifications for fills, errors, escalations, and kill-switch events directly to your iPhone.

## Final Check (Before Live Money)

Before sending live money, ask:
1. Does paper match the backtest?
2. Did the kill switch fire in testing?
3. Is any hard limit delegated to a model instead of code?
4. Is Jev's confidence calibrated on my own fills?
5. What market regime would break this?

Refuse to go live until each answer is clean.
