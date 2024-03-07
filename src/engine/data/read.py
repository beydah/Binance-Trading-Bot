# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
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
FOLDER_PATH = "../.data"
# ----------------------------------------------------------------


def CANDLE(COIN, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None, HEAD_ID=None):
    filePath = WRITE.CANDLE(COIN, CANDLE_PERIOD, DATETIME, CANDLE_LIMIT)
    with open(filePath, "r", newline=''):
        headers = ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
                   "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = LIB.PD.read_csv(filePath, names=headers)
    LIB.OS.remove(filePath)
    if HEAD_ID is None: return df
    return df[headers[HEAD_ID]]
# ----------------------------------------------------------------


def WALLET(COIN=None, HEAD_ID=None):
    filePath = WRITE.WALLET()
    with open(filePath, "r", newline=''):
        headers = ["Coin", "Balance", "USDT_Balance"]
        df = LIB.PD.read_csv(filePath, names=headers)
    if COIN is None and HEAD_ID is None: return df
    elif COIN is not None and HEAD_ID is None: return df[df["Coin"] == COIN]
    elif COIN is None and HEAD_ID is not None: return df[headers[HEAD_ID]]
    return df[df["Coin"] == COIN][headers[HEAD_ID]]


def WALLET_CHANGES(HEAD_ID=None):
    filePath = LIB.OS.path.join(FOLDER_PATH, "WALLET_CHANGES.csv")
    if not LIB.OS.path.exists(filePath): WRITE.WALLET_CHANGES()
    with open(filePath, "r", newline=''):
        headers = ["Total_Balance", "1D_Percent", "3D_Percent",
                   "7D_Percent", "15D_Percent", "30D_Percent", "AVG_Percent"]
        df = LIB.PD.read_csv(filePath, names=headers)
    if HEAD_ID is None: return df.tail(1)
    return df[headers[HEAD_ID]].tail(1)
# ----------------------------------------------------------------


def COINLIST():
    try:
        coinList = []
        with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), "r+") as txtFile:
            for line in txtFile:
                line = line.strip().upper()
                if line and not ("\t" in line):
                    if DATA.FIND_COIN(line): coinList.append(line)
            txtFile.seek(0)
            txtFile.truncate()
            for coin in coinList: txtFile.write(coin + "\n")
        return coinList
    except Exception: MESSAGE.SEND_ERROR(f"Read Coin List: {Exception}")


def COINLIST_CHANGES():
    filePath = LIB.OS.path.join(FOLDER_PATH, "COINLIST_CHANGES.csv")
    if not LIB.OS.path.exists(filePath): WRITE.COINLIST_CHANGES()
    with open(filePath, "r", newline=""):
        headers = ["Coin_Symbol", "7D_Percent", "30D_Percent", "90D_Percent",
                   "180D_Percent", "365D_Percent", "AVG_Percent"]
        return LIB.PD.read_csv(filePath, names=headers)
# ----------------------------------------------------------------


def FAVORITELIST():
    filePath = LIB.OS.path.join(FOLDER_PATH, f"FAVORITELIST.csv")
    if not LIB.OS.path.exists(filePath): WRITE.FAVORITELIST()
    with open(filePath, "r", newline=''): return LIB.PD.read_csv(filePath, names=["Coin"])
# ----------------------------------------------------------------
