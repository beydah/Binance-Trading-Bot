# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
# MESSAGE
from src.engine.message import message as MESSAGE
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


# Binance Data Get Functions
def GET_BINANCE():
    while True:
        try: return API.CLIENT
        except Exception as e: MESSAGE.SEND_ERROR(f"GET_BINANCE: {e}")


def GET_CANDLE(SYMBOL, PERIOD=None, DATETIME=None, LIMIT=None):
    binance = GET_BINANCE()
    if PERIOD is None: PERIOD = DEF.CANDLE_PERIODS[0]
    if LIMIT is None: LIMIT = DEF.CANDLE_LIMIT
    return binance.get_historical_klines(symbol=SYMBOL, interval=PERIOD, end_str=DATETIME, limit=LIMIT)


def GET_SYMBOLINFO(FILTER, COIN):
    binance = GET_BINANCE()
    symbolInfo = binance.get_symbol_info(COIN+"USDT")
    if FILTER == "MIN QTY": return symbolInfo["filters"][1]["minQty"]
    elif FILTER == "MAX QTY": return symbolInfo["filters"][1]["maxQty"]
    else: return None


def GET_ACCOUNT():
    binance = GET_BINANCE()
    clientTimeGap = 0
    while True:
        try: return binance.get_account(timestamp=LIB.TIME.time()-clientTimeGap)
        except Exception as e: clientTimeGap = FIND_TIME_GAP(clientTimeGap, e)


def GET_BALANCES():
    account = GET_ACCOUNT()
    return account["balances"]


def GET_FULLCOIN():
    balances = GET_BALANCES()
    df = LIB.PD.DataFrame(columns=["Coin"])
    for balance in balances: df = df._append({"Coin": balance["asset"]}, ignore_index=True)
    return df
# ----------------------------------------------------------------


# Other Data Get Functions
def FIND_WALLET_CHANGE(NOW_BALANCE, PAST_BALANCES, DAYS):
    try: percentChanges = (NOW_BALANCE - PAST_BALANCES[-DAYS]) / PAST_BALANCES[-DAYS] * 100
    except Exception: percentChanges = 0
    return round(percentChanges, 2)


def FIND_COIN_QUANTITY(USDT_QUANTITY, COIN_PRICE): return float(round(USDT_QUANTITY / COIN_PRICE, 9))


def FIND_USDT_QUANTITY(COIN_QUANTITY, COIN_PRICE): return float(round(COIN_QUANTITY * COIN_PRICE, 9))


def GET_WALLET():
    dfWallet = READ.WALLET()
    wallet = dfWallet.values.reshape(dfWallet.shape[0], dfWallet.shape[1], 1)
    message = ""
    if wallet is not None:
        for i in range(wallet.shape[0]):
            coinInfo = [wallet[i][0], round(float(wallet[i][1]), 8), round(float(wallet[i][2]), 2)]
            message += f"{coinInfo[0]} {coinInfo[1]} - {coinInfo[2]} USD\n"
    MESSAGE.SEND(message)


def GET_COINLIST_INFO():
    try:
        maxCoinList = FIND_MAXLIST()
        minCoinList = FIND_MINLIST()
        MESSAGE.SEND(f"Alert List:\n{maxCoinList}\nFavorite List:\n{minCoinList}\n")
    except Exception as e: MESSAGE.SEND_ERROR(f"GET_COINLIST_INFO: {e}")


def GET_OPEN_ORDER():
    client = GET_BINANCE()
    openOrders = client.get_open_orders()
    if openOrders is None: return None
    orders = []
    for order in openOrders:
        coin = order["symbol"].removesuffix("USDT")
        quantity = float(order["origQty"])
        closePrice = READ.CANDLE(COIN=coin, PERIOD="1m", LIMIT=1, HEAD_ID=4)
        USDTQuantity = float(FIND_USDT_QUANTITY(quantity, closePrice[0]))
        orders.append({"Coin": coin, "Quantity": quantity, "USDT_Quantity": USDTQuantity})
    return LIB.PD.DataFrame(orders)


# ----------------------------------------------------------------


# Data Find Functions
def FIND_TIME_GAP(CLIENT_TIME_GAP, ERROR):
    if CLIENT_TIME_GAP < 5000: return CLIENT_TIME_GAP + 1000
    MESSAGE.SEND_ERROR(f"GET_ACCOUNT: {ERROR}")
    return 0


def FIND_MINLIST():
    try:
        df = READ.COINLIST_CHANGES()
        minAVGList = LIB.HEAP.nsmallest(5, df["AVG_Percent"])
        minCoinList = df.loc[df["AVG_Percent"].isin(minAVGList), ["Coin_Symbol", "AVG_Percent"]]
        df_minCoinList = minCoinList.sort_values("AVG_Percent")
        return df_minCoinList["Coin_Symbol"]
    except Exception as e: MESSAGE.SEND_ERROR(f"FIND_MINLIST: {e}")


def FIND_MAXLIST():
    try:
        df = READ.COINLIST_CHANGES()
        maxAVGList = LIB.HEAP.nlargest(5, df["AVG_Percent"])
        maxCoinList = df.loc[df["AVG_Percent"].isin(maxAVGList), ["Coin_Symbol", "AVG_Percent"]]
        df_maxCoinList = maxCoinList.sort_values("AVG_Percent")
        return df_maxCoinList["Coin_Symbol"]
    except Exception as e: MESSAGE.SEND_ERROR(f"FIND_MAXLIST: {e}")
# ----------------------------------------------------------------
