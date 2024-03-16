# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import write as WRITE
# MATH
from src.engine.math import calculator as CALCULATE
# MESSAGE
from src.engine.message import message as MESSAGE
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def CANDLE(COIN=None, SYMBOL=None, PERIOD=None, DATETIME=None, LIMIT=None, HEAD_ID=None):
    if SYMBOL is None: SYMBOL = COIN + "USDT"
    filePath = WRITE.CANDLE(SYMBOL, PERIOD, DATETIME, LIMIT)
    with open(filePath, "r", newline=''): df = LIB.PD.read_csv(filePath, names=DEF.CANDLE_HEADERS)
    LIB.OS.remove(filePath)
    if HEAD_ID is None: return df
    return df[DEF.CANDLE_HEADERS[HEAD_ID]]
# ----------------------------------------------------------------


def WALLET(COIN=None, HEAD_ID=None):
    filePath = WRITE.WALLET()
    with open(filePath, "r", newline=''): df = LIB.PD.read_csv(filePath, names=DEF.WALLET_HEADERS)
    if COIN is None and HEAD_ID is None: return df
    elif COIN is not None and HEAD_ID is None: return df[df["Coin"] == COIN]
    elif COIN is None and HEAD_ID is not None: return df[DEF.WALLET_HEADERS[HEAD_ID]]
    return df[df["Coin"] == COIN][DEF.WALLET_HEADERS[HEAD_ID]]


def WALLET_CHANGES(HEAD_ID=None):
    filePath = LIB.OS.path.join(DEF.DATA_FOLDER_PATH, "WALLET_CHANGES.csv")
    if not LIB.OS.path.exists(filePath): WRITE.WALLET_CHANGES()
    try:
        with open(filePath, "r", newline=''): df = LIB.PD.read_csv(filePath, names=DEF.WALLET_CHANGES_HEADERS)
        if HEAD_ID is None: return df.tail(1)
        return df[DEF.WALLET_CHANGES_HEADERS[HEAD_ID]].tail(1)
    except Exception as e: MESSAGE.SEND_ERROR(f"WALLET_CHANGES: {e}")
# ----------------------------------------------------------------


def COINLIST():
    OPTIMIZE_COINLIST()
    coinList = []
    try:
        with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), "r+") as txtFile:
            for line in txtFile: coinList.append(line.strip())
        return coinList
    except Exception as e: MESSAGE.SEND_ERROR(f"COINLIST: {e}")


def OPTIMIZE_COINLIST():
    coinList = []
    try:
        with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), "r+") as txtFile:
            for line in txtFile:
                line = line.strip().upper()
                if line and not ("\t" in line):
                    if CALCULATE.FIND_COIN(line): coinList.append(line)
            txtFile.seek(0)
            txtFile.truncate()
            for coin in coinList: txtFile.write(coin+"\n")
    except Exception as e: MESSAGE.SEND_ERROR(f"OPTIMIZE_COINLIST: {e}")


def COINLIST_CHANGES():
    filePath = LIB.OS.path.join(DEF.DATA_FOLDER_PATH, "COINLIST_CHANGES.csv")
    if not LIB.OS.path.exists(filePath): WRITE.COINLIST_CHANGES()
    try:
        with open(filePath, "r", newline=""): return LIB.PD.read_csv(filePath, names=DEF.COINLIST_CHANGES_HEADERS)
    except Exception as e: MESSAGE.SEND_ERROR(f"COINLIST_CHANGES: {e}")
# ----------------------------------------------------------------


def FAVORITELIST():
    filePath = LIB.OS.path.join(DEF.DATA_FOLDER_PATH, f"FAVORITELIST.csv")
    if not LIB.OS.path.exists(filePath): WRITE.FAVORITELIST()
    try:
        with open(filePath, "r", newline=''): return LIB.PD.read_csv(filePath, names=["Coin"])
    except Exception as e: MESSAGE.SEND_ERROR(f"FAVORITELIST: {e}")
# ----------------------------------------------------------------
