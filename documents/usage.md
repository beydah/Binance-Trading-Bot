# Binance Trading Bot

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

## Usage Information

### Binance & Telegram

Our investment bot buys and sells only USDT trading pairs that are not USDT on Binance. Binance API is not just for buying and selling; It is also used to retrieve and calculate historical candle data of the cryptocurrency. As a result of these calculations, coin analysis and coin backtest can be performed. API usage is not limited to these; wallet-related calculations can also be made through wallet reading transactions.

Telegram is used to manage this bot. Currently, it has been created for only one user. It only listens to that user and ignores if another user sends a message. Reads and sends messages from Telegram.

### Coin Backtest & Analysis

After installing this bot, I think the first thing you should do is to measure the risk you take by doing backtesting. This bot is not a superhuman and super intelligent bot; He can lose as much as a human being and gain as much as a human being. For this reason, I recommend you do backtesting to predict the results of the algorithm you will run. To do this, after installing the bot, you can send a message to the bot via Telegram as in the example:

- Message 1: `backtest coin`
- Message 2: `btc, 1000, 100`

If we evaluate the message we sent here, the first content of the message should be the coin name (in this example, our coin is BTC)

The 2nd and 3rd content of the message is optional, just typing BTC is enough. However, by filling in these fields as appropriate, you will have the chance to make better observations.

The 2nd content of the message means your login wallet. It is the first wallet when starting to invest. (In this example our entry wallet is 1000 USDT)

The 3rd content of the message is our monthly addition amount. If you want to add to your wallet when the new month comes, you can fill in this field. If you leave this field blank, you will get the impression that you are investing 100 USDT monthly. Therefore, if you are not going to increase the monthly wallet, it would be better to write 0 in this field. (In this example, our monthly addition is 100 USDT)

Another important process is the analysis part. Thanks to the analysis, I can calculate the instant indicator signals of any coin (except USDT) and return BUY, SELL, None values. In this way, you have the chance to make a prediction based on coin indicators. For analysis, send these messages to the bot via Telegram:

- Message 1: `analysis coin`
- Message 2: `btc`

### Trade Start & Stop

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

## Features Information

### Environment

<table>
    <tr><td></td><td>Package</td><td>Version</td></tr>
    <tr><td>1</td><td>Python</td><td>3.10.0</td></tr>
    <tr><td>2</td><td>pip</td><td>24.0</td></tr>
    <tr><td>3</td><td>python-binance</td><td>1.0.19</td></tr>
    <tr><td>4</td><td>telebot</td><td>0.0.5</td></tr>
    <tr><td>5</td><td>pandas</td><td>2.2.1</td></tr>
    <tr><td>6</td><td>pandas-ta</td><td>0.3.14b0</td></tr>
    <tr><td>7</td><td>requests</td><td>2.31.0</td></tr>
</table>

### Foldering

In this project, great attention was paid to filing. A filing has been made in a way that does not complicate further development of the project. All codes of the project are located in the src folder. Inside the src folder, there is a folder named engine and a main.py file. In the continuation of the project, business, bui etc. under src. Folders will be created, but for now there is only the engine folder. `src/engine/` folder contents:

- `/data/`: In this folder, data reading, writing and fetching operations are performed.
- `/trade/`: This folder contains indicator calculations, other calculations and trade transactions.
- `/bot/`: This folder contains code files related to the telegram bot.
- `/settings/`: This folder contains the settings file with global variables, API variables and libraries.

### Naming

Except for common abbreviations, care has been taken to keep everything descriptive in the nomenclature. It was kept at most 3 words long. Three different nomenclatures were used:

- `CLOSE_PRICE`: Python code pages, libraries, functions are named this way
- `Close_Price`: Global variables, function parameters, headers are named this way.
- `close_price`: Only local variables are named this way.

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

<div style="text-align: center;">
    <a href="#binance-trading-bot">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/scroll_off.png" style="width: 15%;"  alt="^ Scroll UP ^">
    </a>
    <a href="https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/installation.md">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/next_on.png" style="width: 15%;"  alt=">> Continue Reading >>">
    </a>
</div>
