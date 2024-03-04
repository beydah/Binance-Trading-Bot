# ----------------------------------------------------------------
# Added Links
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import analysis as ANALYSIS
from src.engine import algorithm as ALGORITHM
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
# ----------------------------------------------------------------


# Candle Operations
def WRITE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    if CANDLE_LIMIT is None: CANDLE_LIMIT = DEF.CANDLE_LIMIT
    while True:
        try:
            binance = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
            candleList = binance.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD,
                                                       end_str=DATETIME, limit=CANDLE_LIMIT)
            break
        except Exception as e:
            MESSAGE.SEND(f"Error: {e}")
            LIB.SLEEP(15)
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for candleData in candleList:
            candleData[0] = LIB.DATETIME.fromtimestamp(candleData[0] / 1000)
            candleData[6] = LIB.DATETIME.fromtimestamp(candleData[6] / 1000)
            writer.writerow(candleData)
    return filePath


def READ(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None, HEAD_ID=None):
    filePath = WRITE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, CANDLE_LIMIT)
    with open(filePath, "r", newline=''):
        headers = ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
                   "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = LIB.PD.read_csv(filePath, names=headers)
    DELETE(COIN_SYMBOL, CANDLE_PERIOD)
    if HEAD_ID is None: return df
    elif HEAD_ID > -1 and HEAD_ID < 12: return df[headers[HEAD_ID]]


def DELETE(COIN_SYMBOL, CANDLE_PERIOD):
    filePath = LIB.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    if LIB.OS.path.exists(filePath): LIB.OS.remove(filePath)
# ----------------------------------------------------------------
