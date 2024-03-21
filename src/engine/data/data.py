# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MESSAGE
from src.engine.message import message as MSG
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------
Folder_Path = "../.data"
# ----------------------------------------------------------------


# Binance Data Get Functions
def GET_BINANCE():
    while True:
        try: return API.Client
        except Exception as e: MSG.SEND_ERROR(f"GET_BINANCE: {e}")


def GET_CANDLE(Coin, Period=None, Datetime=None, Limit=None):
    binance = GET_BINANCE()
    if Period is None: Period = DEF.Candle_Periods[0]
    if Limit is None: Limit = DEF.Candle_Limit
    while True:
        try: return binance.get_historical_klines(symbol=Coin+"USDT", interval=Period, end_str=Datetime, limit=Limit)
        except Exception as e: MSG.SEND_ERROR(f"GET_CANDLE: {e}")


def GET_SYMBOLINFO(Coin, Info):
    binance = GET_BINANCE()
    while True:
        try:
            symbol_info = binance.get_symbol_info(Coin+"USDT")
            return symbol_info["filters"][1][Info]
        except Exception as e: MSG.SEND_ERROR(f"GET_SYMBOLINFO: {e}")


def GET_OPEN_ORDERS():
    client = GET_BINANCE()
    while True:
        try: return client.get_open_orders()
        except Exception as e: MSG.SEND_ERROR(f"GET_OPEN_ORDER: {e}")


def GET_ACCOUNT():
    binance = GET_BINANCE()
    time_gap = 0
    while True:
        try: return binance.get_account(timestamp=LIB.TIME.time()-time_gap)
        except Exception as e: time_gap = FIND_TIME_GAP(time_gap, e)


def GET_BALANCES():
    account = GET_ACCOUNT()
    return account["balances"]


def GET_FULLCOIN():
    balances = GET_BALANCES()
    df = LIB.PD.DataFrame(columns=["Coin"])
    for balance in balances: df = df._append({"Coin": balance["asset"]}, ignore_index=True)
    return df
# ----------------------------------------------------------------


# Data Get Functions
def GET_WALLET():
    df = READ.WALLET()
    wallet = df.values.reshape(df.shape[0], df.shape[1], 1)
    if wallet is not None: GET_WALLET_MESSAGE(wallet)
    else: MSG.SEND("Wallet Not Found")


def GET_WALLET_MESSAGE(Wallet):
    message = ""
    for i in range(Wallet.shape[0]):
        coin_info = [Wallet[i][0], round(float(Wallet[i][1]), 8), round(float(Wallet[i][2]), 2)]
        message += f"{coin_info[0]} {coin_info[1]} - {coin_info[2]} USD"
    MSG.SEND(message)


def GET_COINLIST_INFO():
    try:
        WRITE.COINLIST_CHANGES()
        WRITE.FAVORITELIST()
        analysis_list = [FIND_MAXLIST(), FIND_MINLIST()]
        MSG.SEND(f"Alert List:\n{analysis_list[0]}\nFavorite List:\n{analysis_list[1]}")
    except Exception as e: MSG.SEND_ERROR(f"GET_COINLIST_INFO: {e}")
# ----------------------------------------------------------------


# Data Find Functions
def FIND_TIME_GAP(Time_Gap, Error):
    if Time_Gap < 5000: return Time_Gap + 1000
    MSG.SEND_ERROR(f"GET_ACCOUNT: {Error}")
    return 0


def FIND_WALLET_CHANGE(Now_Balance, Past_Balances, Day):
    try: return round((Now_Balance - Past_Balances[-Day]) / Past_Balances[-Day] * 100, 2)
    except Exception: return 0


def FIND_COIN_QUANTITY(USDT_Quantity, Coin_Price): return float(round(USDT_Quantity / Coin_Price, 9))


def FIND_USDT_QUANTITY(Coin_Quantity, Coin_Price): return float(round(Coin_Quantity * Coin_Price, 9))


def FIND_MINLIST():
    try:
        df = READ.COINLIST_CHANGES()
        min_avglist = LIB.HEAP.nsmallest(5, df["AVG Percent"])
        min_coinlist = df.loc[df["AVG Percent"].isin(min_avglist), ["Coin", "AVG Percent"]]
        minlist = min_coinlist.sort_values("AVG Percent")
        return minlist["Coin"]
    except Exception as e: MSG.SEND_ERROR(f"FIND_MINLIST: {e}")


def FIND_MAXLIST():
    try:
        df = READ.COINLIST_CHANGES()
        max_avglist = LIB.HEAP.nlargest(5, df["AVG Percent"])
        max_coinlist = df.loc[df["AVG Percent"].isin(max_avglist), ["Coin", "AVG Percent"]]
        maxlist = max_coinlist.sort_values("AVG Percent")
        return maxlist["Coin"]
    except Exception as e: MSG.SEND_ERROR(f"FIND_MAXLIST: {e}")
# ----------------------------------------------------------------
