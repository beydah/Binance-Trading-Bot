# ----------------------------------------------------------------
# Added Links
from src.business import calculator as CALCULATE
from src.business import indicator as INDICATOR
from src.business import backtest as TEST
from src.settings import settings as LIB
from src.settings import api as API
# ----------------------------------------------------------------
# API Connections
CLIENT = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
TELEGRAM_BOT = LIB.BOT.TeleBot(API.TELEGRAM_BOT_KEY)
# ----------------------------------------------------------------


# Candle Transactions
def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    if CANDLE_LIMIT is None: CANDLE_LIMIT = 1000
    if DATETIME is None:
        DATETIME = LIB.TIME.now()
        DATETIME = DATETIME.strftime("%Y-%m-%d %H:%M:%S")
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD,
                                              end_str=DATETIME, limit=CANDLE_LIMIT)
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for candleData in candleList:
            candleData[0] = LIB.TIME.fromtimestamp(candleData[0] / 1000)
            candleData[6] = LIB.TIME.fromtimestamp(candleData[6] / 1000)
            writer.writerow(candleData)
    csvFile.close()
    return filePath


def READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None, HEAD_ID=None):
    filePath = WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, CANDLE_LIMIT)
    with open(filePath, "r", newline='') as csvFile:
        headers = ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
                   "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = LIB.PD.read_csv(filePath, names=headers)
    csvFile.close()
    if HEAD_ID is None: return df
    elif -1 < HEAD_ID < 12: return df[headers[HEAD_ID]]


def DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    filePath = LIB.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    if LIB.OS.path.exists(filePath): LIB.OS.remove(filePath)
# ----------------------------------------------------------------


# Change Transactions
def READ_COINLIST():
    filePath = LIB.OS.path.join("settings", "coinlist.csv")
    with open(filePath, "r", newline='') as csvFile:
        headers = ["Coin_Name"]
        df = LIB.PD.read_csv(filePath, names=headers)
        df = df.apply(lambda x: x.str.strip())
        df = df.dropna()
    csvFile.close()
    return df[headers[0]]


def WRITE_CHANGELIST():
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"CHANGELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        coinList = READ_COINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        CALCULATE.SEND_MESSAGE(f"CHANGELIST File Updating...")
        for i in range(len(coinList)):
            coinSymbol = coinList[i] + "USDT"
            day = [0, 0, 0, 0, 0, 0]
            for j in range(6): day[j] = CALCULATE.GET_CHANGE_PERCENT(coinSymbol, LIB.CHANGELIST_DAYS[j])
            avg = round((day[0] + day[1] + day[2] + day[3] + day[4] + day[5]) / 6, 4)
            writer.writerow([coinSymbol, day[0], day[1], day[2], day[3], day[4], day[5], avg])
        CALCULATE.SEND_MESSAGE("CHANGELIST File Updated.")
    csvFile.close()
    return filePath


def READ_CHANGELIST():
    filePath = WRITE_CHANGELIST()
    with open(filePath, "r", newline="") as csvFile:
        headers = ["Coin_Symbol", "1D_Percent", "7D_Percent", "30D_Percent", "90D_Percent",
                   "180D_Percent", "365D_Percent", "AVG_Percent"]
        df = LIB.PD.read_csv(filePath, names=headers)
    csvFile.close()
    return df


def WRITE_FAVORITELIST():
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        CALCULATE.SEND_MESSAGE(f"FAVORITELIST File Updating...")
        minimumCoinList = CALCULATE.GET_MINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for coin in minimumCoinList: writer.writerow([coin])
        CALCULATE.SEND_MESSAGE(f"FAVORITELIST File Updated.")
    csvFile.close()
# ----------------------------------------------------------------
