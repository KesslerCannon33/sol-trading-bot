# Strategy: SOL Mean-Reversion with Volatility Filter

## Asset
- Symbol: SOL/USD (Solana)
- Exchange: Alpaca Crypto Paper Trading
- Timeframe: 5-minute candles

## Strategy Logic
Conservative mean-reversion: when price deviates significantly from its VWAP,
bet on reversion to the mean, but only in low-volatility regimes.

## Entry Conditions
1. Price is below lower Bollinger Band (2 std dev) — oversold
2. RSI(14) < 35 — confirming oversold
3. Realized volatility (20-period) < 60th percentile of trailing 200 periods
4. Jev regime question returns "ranging" (not "trending")
5. Jev direction question returns "long" with probability > 0.60
6. Jev buying_pressure question returns "yes" with noul > 0.55

## Exit Conditions
1. Price returns to VWAP (take profit)
2. Price hits stop loss (1.5% below entry)
3. RSI > 65 (momentum shifted)
4. Max hold time: 2 hours (24 candles)

## Stop Loss
- 1.5% below entry price

## Take Profit
- Price returns to VWAP

## Jev Questions (Fixed-Outcome)
| Question | Type | Options |
|----------|------|---------|
| regime | choice | trending, ranging, volatile |
| direction | choice | long, short, flat |
| buying_pressure | noul | Is buying pressure real? |
| setup_quality | score | poor, fair, good, excellent |
| risk_state | choice | low, moderate, high, extreme |

## Invalidation Condition
If realized volatility exceeds 90th percentile of trailing 200 periods,
flatten all positions and halt new entries for the remainder of the session.
This indicates a regime change that breaks the mean-reversion assumption.

## Backtest Gates
- Sharpe ratio > 1.5
- Max drawdown < 15%
- Hit rate > 55%
- T-statistic > 2.0 (out of sample)
