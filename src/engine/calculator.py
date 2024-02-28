# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import algotest as TEST
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
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
    if coin == "USDT":
        if BALANCE < 0.01: return 0
        return BALANCE
    coinSymbol = coin + "USDT"
    closePrice = CANDLE.READ(coinSymbol, "1m", None, 1, 4)
    USDTBalance = closePrice[0] * BALANCE
    if USDTBalance < 0.01: return 0
    return USDTBalance


def TOTAL_WALLET(TRANSACTION=None):
    df = WALLET.READ()
    coin = df["Coin"]
    USDTBalance = df["USDT_Balance"]
    totalUSDT = 0
    if TRANSACTION is None:
        for i in range(len(coin)): totalUSDT += USDTBalance[i]
    elif TRANSACTION == 0:
        for i in range(len(coin)):
            if coin[i][:2] != "LD": totalUSDT += balance[i]
    elif TRANSACTION == 1:
        for i in range(len(coin)):
            if coin[i][:2] == "LD": totalUSDT += balance[i]
    totalUSDT = round(totalUSDT, 2)
    return totalUSDT
# ----------------------------------------------------------------


# Get Calculations
def GET_CHANGE_PERCENT(COIN_SYMBOL, DAYS):
    past = LIB.TIMEDELTA(days=DAYS)
    today = LIB.DATETIME.now()
    past_date = today - past
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    past_date = past_date.strftime("%Y-%m-%d %H:%M:%S")
    try:
        pastPrices = CANDLE.READ(COIN_SYMBOL, "1m", past_date, 1, 4)
        currentPrices = CANDLE.READ(COIN_SYMBOL, "1m", today, 1, 4)
        pastPrice = pastPrices[len(pastPrices) - 1]
        currentPrice = currentPrices[len(currentPrices) - 1]
        priceDifference = currentPrice - pastPrice
        percentChange = round((priceDifference / pastPrice) * 100, 4)
    except Exception: percentChange = 0
    return percentChange


def GET_MINLIST():
    df = LIST.READ_CHANGE()
    maxAVGList = LIB.HEAP.nlargest(5, df["AVG_Percent"])
    maxCoinList = df.loc[df["AVG_Percent"].isin(maxAVGList), ["Coin_Symbol", "AVG_Percent"]]
    minAVGList = LIB.HEAP.nsmallest(5, df["AVG_Percent"])
    minCoinList = df.loc[df["AVG_Percent"].isin(minAVGList), ["Coin_Symbol", "AVG_Percent"]]
    df_minCoinList = minCoinList.sort_values("AVG_Percent")
    MESSAGE.SEND(f"Alert List: \n{maxCoinList}")
    MESSAGE.SEND(f"Favorite List: \n{minCoinList}")
    return df_minCoinList["Coin_Symbol"]


def GET_SYMBOL_FROM_ID(SYMBOL_ID):
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    if not LIB.OS.path.exists(filePath): LIST.WRITE_FAVORITE()
    with open(filePath, "r", newline=""):
        headers = ["Coin_Symbol"]
        df = LIB.PD.read_csv(filePath, names=headers)
    favoriteCoins = df["Coin_Symbol"].tolist()
    return favoriteCoins[SYMBOL_ID]
# ----------------------------------------------------------------
