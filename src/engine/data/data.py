# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
# MESSAGE
from src.engine.message import message as MSG
from src.engine.message import transactions as T
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------
Folder_Path = "src/.data"
# ----------------------------------------------------------------


def GET_BINANCE():
    while True:
        try: return API.Binance
        except Exception as e: MSG.SEND_ERROR(f"GET_BINANCE: {e}")


def GET_CANDLE(Coin, Period=None, Limit=None, Datetime=None):
    binance = GET_BINANCE()
    if Period is None: Period = DEF.Candle_Periods[0]
    if Limit is None: Limit = DEF.Candle_Limit
    while True:
        try: return binance.get_historical_klines(symbol=Coin + "USDT", interval=Period, end_str=Datetime, limit=Limit)
        except Exception as e: MSG.SEND_ERROR(f"GET_CANDLE: {e}")


def GET_SYMBOL_INFO(Coin, Info):
    binance = GET_BINANCE()
    while True:
        try: return binance.get_symbol_info(Coin + "USDT")["filters"][1][Info]
        except Exception as e: MSG.SEND_ERROR(f"GET_SYMBOLINFO: {e}")


def GET_OPEN_ORDERS(Symbol=None):
    binance = GET_BINANCE()
    while True:
        try: return binance.get_open_orders(symbol=Symbol)
        except Exception as e: MSG.SEND_ERROR(f"GET_OPEN_ORDER: {e}")


def GET_ACCOUNT():
    binance = GET_BINANCE()
    time_gap = 0
    while True:
        try: return binance.get_account(timestamp=LIB.TIME.time() - time_gap)
        except Exception as e:
            if time_gap < 5000: time_gap += 1000
            else:
                time_gap = 0
                MSG.SEND_ERROR(f"GET_ACCOUNT: {e}")


def GET_BALANCES():
    account = GET_ACCOUNT()
    return account["balances"]


def GET_FULLCOIN():
    balances = GET_BALANCES()
    df = LIB.PD.DataFrame(columns=[DEF.Wallet_Headers[0]])
    for balance in balances: df = df._append({DEF.Wallet_Headers[0]: balance["asset"]}, ignore_index=True)
    return df
# ----------------------------------------------------------------


def GET_WALLET_INFO():
    df = READ.WALLET()
    T.Transaction[T.Wallet] = True
    wallet = df.values.reshape(df.shape[0], df.shape[1], 1)
    if wallet is not None:
        message = ""
        for i in range(wallet.shape[0]):
            coin_info = [wallet[i][0], round(float(wallet[i][1]), 8), round(float(wallet[i][2]), 2)]
            message += f"{coin_info[0]} {coin_info[1]} - {coin_info[2]} USD\n"
        MSG.SEND(message)
    else: MSG.SEND("Wallet is None")
    T.Transaction[T.Wallet] = False


def GET_COINLIST_INFO():
    T.Transaction[T.Coinlist] = True
    try: MSG.SEND(f"Alert List:\n{CALCULATE.MAXLIST()}\nFavorite List:\n{CALCULATE.MINLIST()}")
    except Exception as e: MSG.SEND_ERROR(f"GET_COINLIST_INFO: {e}")
    T.Transaction[T.Coinlist] = False
# ----------------------------------------------------------------


def FIND_WALLET_CHANGE(Now_Balance, Past_Balances, Day):
    try: return round((Now_Balance - Past_Balances[-Day]) / Past_Balances[-Day] * 100, 2)
    except Exception: return 0


def FIND_COIN_QUANTITY(USDT_Quantity, Coin_Price): return float(round(USDT_Quantity / Coin_Price, 9))


def FIND_USDT_QUANTITY(Coin_Quantity, Coin_Price): return float(round(Coin_Quantity * Coin_Price, 9))
# ----------------------------------------------------------------
