# Real SOL trading connection — current status

Real trading is not enabled. Free Pump.fun discovery continues independently.
For SOL itself, the proposed market is SOL/USDC on Solana through Jupiter.
The quote adapter is in `src/trading_bot/brokers/jupiter_client.py`; it performs
only GET quote requests, never signs or submits transactions.

The agreed limits are saved in `config/risk.yaml`: $1,000 capital allocation,
$500 absolute entry cap, and the existing 5% position rule, initially $50.
Capital allocation limits exposure; it does not guarantee a maximum loss.

## Missing connection information

- Wallet selected: **Phantom on a phone**. Use its in-app browser to connect.
- Public wallet address (safe to share, but identifies public on-chain activity).
- `JUPITER_API_KEY` configured locally through the environment or `.env`.
- A Solana RPC connection for confirmed balances and transaction reconciliation.

Do not paste wallet seed phrases or private keys into chat. Browser-wallet
signing and unattended server signing need different implementations; choosing
the signing method is necessary before connecting execution.

## Phantom connection screen

The dashboard now serves `/wallet`, with Phantom connection/disconnection,
account-change handling and a quote preview. Connection only reads the public
address in the browser; it does not sign messages or transactions or send the
wallet address to this server. Quote requests need `JUPITER_API_KEY` locally and
are limited to $50 initially by the saved percentage rule. USDC is treated as
$1 only for the quote preview; this is not a live execution valuation.

On a phone, open the page inside Phantom's browser using a reachable HTTPS URL.
The workspace's `http://127.0.0.1:8000/wallet` address is local to the workspace
and will not work on the phone. HTTPS hosting / forwarding is not configured.
Phantom provider access does not work in a cross-origin iframe. See
[Phantom provider detection](https://docs.phantom.com/solana/detecting-the-provider).

## Implementation still required before activation

Connect wallet signing, validate transactions against the intended pair and
amount, reserve network fees, persist pending order IDs, reconcile confirmed
fills and balances, and enforce budget and drawdown checks on actual marked
equity. Fix the existing paper broker's zero-unrealized-P&L model for meaningful
forward testing. The strategy has not demonstrated an edge on real data.

Jupiter's official flow is quote/assemble, sign, then execute. Without `taker`,
its order endpoint returns a price quote without a wallet transaction.
[Official integration documentation](https://developers.jup.ag/docs/swap/order-and-execute).

Do not add an `ENABLE_LIVE=true` variable expecting it to create this connection;
no such implemented switch exists.
