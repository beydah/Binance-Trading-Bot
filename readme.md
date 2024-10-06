# Binance Trading Bot

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/banner/binance-trading-bot-upper.png" alt="Banner">
    </a>
</div>

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

## Fast Information
### Binance Trading Bot

This bot, which can be managed via Telegram, creates Buy/Sell signals using indicators such as 
RSI, StochRSI, EMA, MA and can make buying and selling decisions based on these signals; can do backtesting; 
Can analyze coins. **It is not investment advice. It has risks and losses.**

This project was created and developed by Beydah Saglam. He still continues to develop this project. 
**Solutions for which you can sponsor the developer will be introduced soon.**

### For Support
- To provide support to the developer, you can follow it at [github/beydah](https://github.com/beydah).
- **You can star the project to support the project.**

### News 
**Version 1.0.5 - Date 17.05.2024**

**Main Title:** Update to Indicator Signals and Settings
- I created a setting range that I believe will provide more profit in indicator signals.
- I adjusted the signals so that it can capture every signal, not just the first signal.

````python
"""
def DCA_SIGNAL(Old_Prices, Prices, Old_SMA25, SMA25):
    if Old_Prices < Old_SMA25 and Prices > SMA25: return 1
    if Old_Prices > Old_SMA25 and Prices < SMA25: return -1
    return 0
"""

def DCA_SIGNAL(Prices, SMA25):
    if Prices > SMA25: return 1
    elif Prices < SMA25: return -1
    return 0
````

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

## Links of Contents
### Usage
- [Usage Information](https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/usage.md#usage-information)
- [Features Information](https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/usage.md#features-information)

### Installation
- [Download Steps](https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/installation.md#download-steps)
- [Installation Steps](https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/installation.md#installation-steps)

### Agreement
- [Disclaimer](https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/agreement.md#disclaimer)
- [License](https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/agreement.md#license)

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

<div style="text-align: center;">
    <a href="#binance-trading-bot">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/scroll_off.png" style="width: 15%;"  alt="^ Scroll UP ^">
    </a>
    <a href="https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/usage.md">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/next_on.png" style="width: 15%;"  alt=">> Continue Reading >>">
    </a>
</div>
