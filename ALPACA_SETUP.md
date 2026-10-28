# SOL paper trading on Alpaca

The URL `https://paper-api.alpaca.markets/v2` is an API address, not an API key.
The adapter fixes Alpaca's SDK to `paper=True`; no live endpoint is configurable.

1. Sign in to your Alpaca account and select **Paper Trading**.
2. In its **API Keys** panel, generate a **Key ID** and **Secret Key** for that
   paper account. Keep both out of chat.
3. Configure those values as secure environment variables in the execution
   environment, or edit the project's private `.env` file locally:

```dotenv
ALPACA_API_KEY=your_paper_key_id
ALPACA_API_SECRET=your_paper_secret_key
```

`ALPACA_API_SECRET` is this project's name for Alpaca's Secret Key. The endpoint
is fixed by the code; no endpoint credential is needed. Use a dedicated paper
account with no open positions or pending orders. Existing holdings cause startup
to stop; the bot does not automatically adopt or close them at startup.

Check authentication, tradability, and completed SOL candles without placing any
orders:

```bash
cd /workspace/trading-bot
.venv/bin/python -m trading_bot.main --check-alpaca
```

After that succeeds, start the SOL paper loop:

```bash
.venv/bin/python -m trading_bot.main --alpaca-paper
```

Dashboard: http://127.0.0.1:8000, local to the machine running the bot. Stop another
dashboard process on this port first. Phone access still requires reachable HTTPS
hosting. Alpaca does not use Phantom; no wallet funding or wallet signing is
needed for paper trading.

The agreed capital allocation is $1,000, with an absolute $500 entry ceiling.
The 5% position rule remains tighter, initially allowing up to $50 per position.
Alpaca may show a larger paper account balance; this bot uses the allocated
balance plus changes in that dedicated account's marked equity. The initial
account-equity baseline is saved in SQLite, so restarting does not erase losses
from allocated equity. Manual account resets/deposits or other trades invalidate
this allocation accounting: reconcile the account and baseline before resuming.
Daily loss and peak-drawdown state are not fully persisted across restarts; this
adapter is for supervised paper testing, not a production live-money system.

Entries are price-bounded IOC limit orders. They may fill partially or not at
all, rather than paying more than the entry limit. Exits use IOC market orders.
Actual filled quantities and average prices update positions. Uncertain
submissions block further execution; check the order in Alpaca before restarting.
A kill-switch closure request is not proof of a confirmed flat account: inspect
the paper account after a halt. Stopping the process does not close holdings.

The `--alpaca-paper` command deliberately uses MockJev and disables external AI
and Telegram calls. This tests plumbing and the existing rules; it is not model
training or evidence of profitability. The synthetic backtest remains synthetic.
The adapter and partial-fill/risk behaviors were verified with mocked Alpaca SDK
responses. Authenticated verification succeeded on October 7, 2026: SOL/USD was tradable, 250 completed candles were retrieved, and allocated equity was $1,000. That check placed no orders. Credentials posted in chat should be rotated in Alpaca before ongoing use.

References: [Alpaca paper trading](https://docs.alpaca.markets/us/docs/paper-trading),
[getting started / API keys](https://docs.alpaca.markets/us/docs/getting-started-with-trading-api),
[crypto order types](https://docs.alpaca.markets/us/docs/orders-at-alpaca),
[official crypto market-data SDK](https://alpaca.markets/sdks/python/api_reference/data/crypto/historical.html).

### Optional official TypeSafe Jev scoring

The bot connects the two services: Alpaca supplies completed SOL/USD candles,
Jev scores the market snapshot, and the bot checks strategy and budget limits
before submitting an Alpaca paper order. Add your official TypeSafe key as
`JEV_API_KEY` in your private `.env`, alongside your newly rotated Alpaca paper
Key ID and Secret Key. Keep credentials out of chat and the downloadable ZIP.
The client uses https://api.typesafe.ai/v1/systemone; independent gateway keys
are not interchangeable with official TypeSafe keys.

Run `.venv/bin/python -m trading_bot.main --alpaca-paper --use-jev`.
This opts into paid scoring calls. Without `--use-jev`, paper mode uses mock
scoring and cannot establish Jev performance. Malformed Jev answers reject
that decision. Model confidence is not a demonstrated trading win rate;
profitability and confidence-based sizing still require empirical validation.
The $1,000 allocation, $500 ceiling and tighter 5% position limit remain.
Trading stays paused until credentials are configured and the command is run.
