# Binance Trading Bot

<div align="center">
    <img src="https://raw.githubusercontent.com/beydah/asset/main/banner/binance-trading-bot-upper.png" alt="Banner" width="100%">
    <br>
    <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick" width="80%">
    <br>
    
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**An advanced, modular, and secure algorithmic trading bot for Binance Spot & Margin markets.**

[Installation](documents/installation.md) • [Usage](documents/usage.md) • [Contributing](CONTRIBUTING.md) • [Security](SECURITY.md)

</div>

## 🚀 Features

-   **Algorithmic Trading**: Utilizes RSI, StochRSI, EMA, SMA, and "Golden Cross" strategies.
-   **Risk Management**: Integrated Stop Loss and Take Profit mechanisms (Trailing Stop optimization).
-   **Scheduler**: Automated tasks for daily/hourly market analysis without blocking loops.
-   **Backtesting**: Simulate strategies on historical data before risking real funds.
-   **Secure**: API keys managed via environment variables (`.env`), not hardcoded.
-   **Telegram Integration**: Full control and monitoring via Telegram commands.

## 🛠️ Quick Start

1.  **Clone & Install**:
    ```bash
    git clone https://github.com/beydah/Binance-Trading-Bot.git
    cd Binance-Trading-Bot
    pip install -r requirements.txt
    ```

2.  **Configure**:
    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```

3.  **Run**:
    ```bash
    python src/main.py
    ```

Full guide: [Installation Guide](documents/installation.md)

## 📂 Project Structure

```
Binance-Trading-Bot/
├── documents/          # Detailed documentation
├── src/
│   ├── main.py         # Entry point
│   ├── config.py       # Configuration management
│   ├── bot/            # Telegram bot logic
│   ├── engine/         # Trading engine Core
│   ├── data/           # Data persistence layer
│   └── utils/          # Utilities (Logger, etc.)
├── tests/              # Unit tests
├── .env.example        # Environment template
└── requirements.txt    # Dependencies
```

## ⚠️ Disclaimer

**This software is for educational purposes only.** Cryptocurrency trading involves significant risk. The developers are not responsible for any financial losses incurred while using this bot. Always backtest and use at your own risk.

Read full [User Agreement](documents/agreement.md).

<div align="center">
    <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick" width="80%">
    <br>
    <h3>Developed by <a href="https://github.com/beydah">Beydah Saglam</a></h3>
</div>
