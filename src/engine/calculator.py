# ----------------------------------------------------------------
# Added Links
from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
from src.engine import dataops as DATA
# ----------------------------------------------------------------


# Order Calculations
def TEST_BUY(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY / WEALTH_PRICE
    commission = coinQuantity * DEF.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    coinQuantity = round(coinQuantity, 6)
    return coinQuantity


def TEST_SELL(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY * WEALTH_PRICE
    commission = coinQuantity * DEF.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    coinQuantity = round(coinQuantity, 6)
    return coinQuantity
# ----------------------------------------------------------------


# Wallet Calculations
def FIND_USDT_BALANCE(COIN, BALANCE):
    if COIN[:2] == "LD": coin = COIN[2:]
    else: coin = COIN
    if coin == "USDT": return BALANCE
    coinSymbol = coin + "USDT"
    closePrice = DATA.READ_CANDLE(coinSymbol, "1m", None, 1, 4)
    USDTBalance = closePrice[0] * BALANCE
    if USDTBalance < 0.01: return 0
    else: return USDTBalance


def TOTAL_WALLET(TRANSACTION=None):
    df = DATA.READ_WALLET()
    coin = df["Coin"]
    balance = df["Balance"]
    totalUSDT = 0
    if TRANSACTION is None:
        for i in range(len(coin)):
            if coin[i][:2] == "LD": symbol = coin[i][2:]
            else: symbol = coin[i]
            if symbol == "USDT":
                totalUSDT += balance[i]
                continue
            coinSymbol = symbol + "USDT"
            closePrice = DATA.READ_CANDLE(coinSymbol, "1m", None, 1, 4)
            USDTBalance = closePrice[0] * balance[i]
            totalUSDT += USDTBalance
    elif TRANSACTION == 0:
        for i in range(len(coin)):
            if coin[i][:2] == "LD": continue
            if coin[i] == "USDT":
                totalUSDT += balance[i]
                continue
            coinSymbol = coin[i] + "USDT"
            closePrice = DATA.READ_CANDLE(coinSymbol, "1m", None, 1, 4)
            USDTBalance = closePrice[0] * balance[i]
            totalUSDT += USDTBalance
    elif TRANSACTION == 1:
        for i in range(len(coin)):
            if coin[i][:2] != "LD": continue
            symbol = coin[i][2:]
            if symbol == "USDT":
                totalUSDT += balance[i]
                continue
            coinSymbol = symbol + "USDT"
            closePrice = DATA.READ_CANDLE(coinSymbol, "1m", None, 1, 4)
            USDTBalance = closePrice[0] * balance[i]
            totalUSDT += USDTBalance
    totalUSDT = round(totalUSDT, 2)
    return totalUSDT
# Hesaplamaları DATA.WRITE_TOTAL_BALANCE içine gönder.
# ----------------------------------------------------------------


# Message Calculations
def MESSAGE(BOT_MESSAGE):
    print(BOT_MESSAGE)
    try:
        URL = (f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
               f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
               f"&parse_mode=Markdown&text={BOT_MESSAGE}")
        LIB.REQUEST.get(URL)
    except Exception as e: print(f"Error: {e}")


def TEST_MESSAGE(ALGORITHM_NAME, LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                 TOTAL_COIN, TOTAL_INVESMENT, BUY_NUM, SELL_NUM, CLOSE_PRICE):
    WALLET = round(WALLET, 2)
    coinWallet = TOTAL_COIN * CLOSE_PRICE
    coinWallet = round(coinWallet, 2)
    TOTAL_COIN = round(TOTAL_COIN, 6)
    message = (f"Algorithm: {ALGORITHM_NAME}\n"
               f"Symbol: {LEFT_SMYBOL + RIGHT_SYMBOL} - Period: {CANDLE_PERIOD}\n"
               f"Total Transactions: {BUY_NUM + SELL_NUM}\n"
               f"Total Investment: {TOTAL_INVESMENT} - {RIGHT_SYMBOL}\n")
    if TOTAL_COIN != 0: message += (f"Total Coin: {TOTAL_COIN} - {LEFT_SMYBOL}\n"
                                    f"Current Wallet: {coinWallet} - {RIGHT_SYMBOL}")
    else: message += f"Current Wallet: {WALLET} - {RIGHT_SYMBOL}"
    MESSAGE(message)
# ----------------------------------------------------------------


# Get Calculations
def GET_CHANGE_PERCENT(COIN_SYMBOL, DAYS):
    past = LIB.TIMEDELTA(days=DAYS)
    today = LIB.DATETIME.now()
    past_date = today - past
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    past_date = past_date.strftime("%Y-%m-%d %H:%M:%S")
    try:
        pastPrices = DATA.READ_CANDLE(COIN_SYMBOL, "1m", past_date, 1, 4)
        currentPrices = DATA.READ_CANDLE(COIN_SYMBOL, "1m", today, 1, 4)
        pastPrice = pastPrices[len(pastPrices) - 1]
        currentPrice = currentPrices[len(currentPrices) - 1]
        priceDifference = currentPrice - pastPrice
        percentChange = round((priceDifference / pastPrice) * 100, 4)
    except Exception: percentChange = 0
    return percentChange


def GET_MINLIST():
    df = DATA.READ_CHANGELIST()
    maxAVGList = LIB.HEAP.nlargest(5, df["AVG_Percent"])
    maxCoinList = df.loc[df["AVG_Percent"].isin(maxAVGList), ["Coin_Symbol", "AVG_Percent"]]
    minAVGList = LIB.HEAP.nsmallest(5, df["AVG_Percent"])
    minCoinList = df.loc[df["AVG_Percent"].isin(minAVGList), ["Coin_Symbol", "AVG_Percent"]]
    df_minCoinList = minCoinList.sort_values("AVG_Percent")
    MESSAGE(f"Alert List: \n{maxCoinList}")
    MESSAGE(f"Favorite List: \n{minCoinList}")
    return df_minCoinList["Coin_Symbol"]


def GET_SYMBOL_FROM_ID(SYMBOL_ID):
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    if LIB.OS.path.exists(filePath) is False: DATA.WRITE_FAVORITECOINS()
    with open(filePath, "r", newline="") as csvFile:
        headers = ["Coin_Symbol"]
        df = LIB.PD.read_csv(filePath, names=headers)
    csvFile.close()
    favoriteCoins = df["Coin_Symbol"].tolist()
    return favoriteCoins[SYMBOL_ID]
# ----------------------------------------------------------------
