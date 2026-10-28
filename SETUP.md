# Solana / Pump.fun setup

Installed in `/workspace/trading-bot` with an isolated `.venv`. Start here:

```bash
cd /workspace/trading-bot
.venv/bin/python -m trading_bot.main --pumpfun
```

Dashboard: http://127.0.0.1:8000. This command defaults to **free discovery only**,
showing newly created token mint addresses through PumpPortal. It does not
select investments or place wallet transactions. Status and discoveries are also
available at `/api/status`.

For paper trading ONE selected Pump.fun token, edit `.env` locally:

```dotenv
PUMPFUN_MINT=the_token_mint_address
PUMPPORTAL_API_KEY=your_key
PUMPFUN_ENABLE_PAID_DATA=true
```

Those values stay saved between restarts. Never put a seed phrase or private key
in this configuration. The implementation has no wallet signing or transaction
submission path. Pump.fun tokens trade on Solana; this does not trade SOL itself,
XRP, XMR, Ethereum assets, or Robinhood holdings.

PumpPortal's trade feed requires its API key and linked wallet funded with at
least 0.02 SOL; the documented data charge is 0.01 SOL per 10,000 events.
Turning on paid data authorizes that provider's data charges, even though fills
are simulated. See https://pumpportal.fun/data-api/real-time/.

The saved allocation is $1,000 and the absolute trade ceiling is $500 in
`config/risk.yaml`. The existing 5% position rule remains tighter: initially
$50 maximum exposure on $1,000, or $25 on a $500 allocation. These are exposure
limits, not trade-count limits or guaranteed loss caps. Proceeds can be reused
after an exit, subject to fees, available cash and risk checks.

Paper mode starts with the configured allocation as simulated equity, uses MockJev and retains the
original risk checks, including manual-approval blocking. Trade amounts are
converted to USD using Coinbase's public SOL/USD spot quote refreshed every
60 seconds. Candles use receipt time and observed trade amounts. This is not
historical on-chain data or an executable quote; fees, slippage, liquidity and
network costs are not simulated. A continuous 201 closed five-minute bars
(about 17 hours) are needed before strategy signals. Missing candle intervals
or reconnects reset warmup. The existing strategy has not been validated for
Pump.fun tokens. Discovery requires no key; paid trading cannot be verified
until a key and selected mint are configured.

```bash
.venv/bin/pytest -q
```

Keep the dashboard on localhost. This workspace process is not a permanent
24/7 deployment. Stop it with Ctrl+C; simulated positions are kept in memory
and disappear on restart.
