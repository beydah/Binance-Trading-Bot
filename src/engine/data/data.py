# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import indicator as INDICATOR
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import bot as BOT
from src.engine.message import message as MESSAGE
from src.engine.message import transactions as TRANSACTIONS
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# THREAD
from src.engine.thread import timer as TIMER
from src.engine.thread import debugger as DEBUGGER
from src.engine.thread import processor as PROCESSOR
# ----------------------------------------------------------------
# Global Object
CLIENT = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
# ----------------------------------------------------------------


def GET_BINANCE():
    while True:
        try: return CLIENT
        except Exception: MESSAGE.SEND_ERROR(f"Data Get Binance: {Exception}")


def GET_CANDLE(COIN, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    if CANDLE_LIMIT is None: CANDLE_LIMIT = DEF.CANDLE_LIMIT
    binance = GET_BINANCE()
    return binance.get_historical_klines(symbol=COIN+"USDT", interval=CANDLE_PERIOD,
                                               end_str=DATETIME, limit=CANDLE_LIMIT)


def GET_ACCOUNT():
    binance = GET_BINANCE()
    return binance.get_account(timestamp=LIB.TIME.time() - 1000)


def GET_BALANCES():
    account = GET_ACCOUNT()
    return account["balances"]


def GET_FULLCOIN():
    df = LIB.PD.DataFrame(columns=["Coin"])
    balances = GET_BALANCES()
    for balance in balances: df = df._append({"Coin": balance["asset"]}, ignore_index=True)
    return df
# ----------------------------------------------------------------


def GET_WALLET(): return READ.WALLET()  # MESSAGE.SEND(READ.WALLET())


def GET_USDT_BALANCE(COIN, BALANCE): return CALCULATE.USDT_BALANCE(COIN, BALANCE)


def GET_TOTAL_WALLET(TRANSACTION_ID): return CALCULATE.TOTAL_WALLET(TRANSACTION_ID)


def GET_WALLET_CHANGE(NOW_BALANCE, PAST_BALANCES, DAYS):
    try: percentChanges = round((NOW_BALANCE - PAST_BALANCES[-DAYS]) / PAST_BALANCES[-DAYS] * 100, 2)
    except Exception: percentChanges = 0
    return percentChanges


def GET_COIN_CHANGE(COIN, DAYS): return CALCULATE.COIN_CHANGE(COIN, DAYS)


def GET_COINLIST_INFO():
    WRITE.COINLIST_CHANGES()
    maxCoinList = FIND_MAXLIST()
    minCoinList = FIND_MINLIST()
    MESSAGE.SEND(f"Alert List:\n{maxCoinList}\nFavorite List:\n{minCoinList}\n")


def GET_COIN_INFO(COIN): return CALCULATE.COIN_INFO(COIN)


def GET_WALLET_INFO(): return CALCULATE.WALLET_INFO()


def GET_COIN_FROM_FAVORITELIST(COIN_ID):
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    if not LIB.OS.path.exists(filePath): WRITE.FAVORITELIST()
    with open(filePath, "r", newline=""): df = LIB.PD.read_csv(filePath, names=["Coin_Symbol"])
    favoriteCoins = df["Coin_Symbol"].tolist()
    return favoriteCoins[COIN_ID]
# ----------------------------------------------------------------


def FIND_COIN(COIN): return CALCULATE.SEARCH_COIN(COIN)


def FIND_MINLIST():
    df = READ.COINLIST_CHANGES()
    minAVGList = LIB.HEAP.nsmallest(5, df["AVG_Percent"])
    minCoinList = df.loc[df["AVG_Percent"].isin(minAVGList), ["Coin_Symbol", "AVG_Percent"]]
    df_minCoinList = minCoinList.sort_values("AVG_Percent")
    return df_minCoinList["Coin_Symbol"]


def FIND_MAXLIST():
    df = READ.COINLIST_CHANGES()
    maxAVGList = LIB.HEAP.nlargest(5, df["AVG_Percent"])
    maxCoinList = df.loc[df["AVG_Percent"].isin(maxAVGList), ["Coin_Symbol", "AVG_Percent"]]
    df_maxCoinList = maxCoinList.sort_values("AVG_Percent")
    return df_maxCoinList["Coin_Symbol"]
# ----------------------------------------------------------------
