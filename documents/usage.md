# Usage Guide

## Telegram Commands

The bot is primarily controlled via Telegram messages. Ensure you are sending messages from the account ID specified in your `.env` file.

### General Commands

-   **Trade Control**:
    -   `Open Trade`: Starts the trading loop. The bot will begin analyzing market conditions and executing trades.
    -   `Close Trade`: Stops the trading loop. The bot will stop looking for new buy/sell signals. Note: This does not close open positions immediately.

### Analysis & Backtesting

-   **Backtest**:
    Simulate the strategy on historical data.
    -   Format: `backtest <coin>, <start_capital>, <monthly_addition>`
    -   Example: `backtest BTC, 1000, 100`

-   **Analysis**:
    Get an instant analysis of a specific coin based on current indicators.
    -   Format: `analysis <coin>`
    -   Example: `analysis ETH`

## Trading Strategy

The bot uses a combination of indicators to identify entry and exit points:

-   **Indicators**: RSI, StochRSI, EMA (Exponential Moving Average), SMA (Simple Moving Average), and "Golden Cross" detection.
-   **Buy Signal**: Generally triggered when indicators suggest oversold conditions or a bullish trend reversal (e.g., Golden Cross + Low RSI).
-   **Sell Signal**: Triggered when indicators suggest overbought conditions, trend reversal, or when Stop Loss/Take Profit targets are hit.

## Troubleshooting

-   **Bot not responding**: Check the console logs (`logs/bot.log`) for errors. Ensure your Telegram Token is correct.
-   **API Errors**: specific Binance errors usually mean your IP address is not whitelisted or your API permissions are incorrect.
