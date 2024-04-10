# Binance Trading Bot

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/banner/binance-trading-bot-upper.png" alt="Colorful Stick">
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
**Version 1.0.4 - Date 10.04.2024**

**Main Title:** Bug Fix Timestamp Error, Rising Stop Loss Code Block
- **"APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time."** error has been resolved
absolutely. In previous solutions, it was necessary to constantly update the time on the user computer and an attempt 
was made to subtract the time from the user time zone. Now we pull the Binance server time and display this time 
instead:

````python
def GET_SERVER_TIME():
    binance = GET_BINANCE()
    while True:
        try: return binance.get_server_time()["serverTime"]
        except Exception as e: MSG.SEND_ERROR(f"GET_BINANCE_SERVER_TIME: {e}")

def GET_ACCOUNT():
    binance = GET_BINANCE()
    time_gap = 0
    while True:
        try: return binance.get_account(timestamp=GET_BINANCE_SERVER_TIME() - time_gap)
        except Exception as e: time_gap = FIND_TIME_GAP(Time_Gap=time_gap, Error=f"GET_ACCOUNT: {e}")
````

- In order not to compromise on profits in trade transactions, the code block that will constantly increase the Stop 
Loss level has been added to the Beyza_Start function:

````python
last_price = DATA.GET_STOP_LOSS_ORDER(wallet[headers[0]][i])
price = READ.CANDLE(Coin=wallet[headers[0]][i], Limit=1, Head_ID=4)[0]
if last_price is None: last_price = float(price) * 0.95
else: last_price = last_price['price']
if (float(price) * 0.98) >= float(last_price):
    CALCULATE.DELETE_STOP_LOSS(wallet[headers[0]][i])
    CALCULATE.STOP_LOSS(wallet[headers[0]][i])
````

- Errors in Delete_Stop_Loss and Get_Stop_Loss functions have been fixed.
- With the new update, the bot will now wait 250 seconds when the Send_Error function runs.
- The requirements.txt file has been updated to install compatible versions of the required libraries.

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
