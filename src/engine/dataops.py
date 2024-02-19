# ----------------------------------------------------------------
# Added Links
from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
from src.engine import calculator as CALCULATE
# ----------------------------------------------------------------
# API Connections
CLIENT = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
TELEGRAM_BOT = LIB.BOT.TeleBot(API.TELEGRAM_BOT_KEY)
# ----------------------------------------------------------------


# Candle CRUDs
def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    if CANDLE_LIMIT is None: CANDLE_LIMIT = DEF.CANDLE_LIMIT
    if DATETIME is None:
        DATETIME = LIB.TIME.now()
        DATETIME = DATETIME.strftime("%Y-%m-%d %H:%M:%S")
    while True:
        try:
            candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD,
                                                      end_str=DATETIME, limit=CANDLE_LIMIT)
            break
        except Exception:
            CALCULATE.SEND_MESSAGE(f"Error 1: {Exception} - Internet / Binance Connection Could Not Be Established.")
            LIB.SLEEP(15)
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
    elif HEAD_ID > -1 and HEAD_ID < 12: return df[headers[HEAD_ID]]


def DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    try:
        filePath = LIB.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
        if LIB.OS.path.exists(filePath): LIB.OS.remove(filePath)
    except Exception: pass
# ----------------------------------------------------------------


# Change CRUDs
def READ_COINLIST():
    filePath = LIB.OS.path.join("settings", "coinlist.txt")
    if not LIB.OS.path.exists(filePath):
        CALCULATE.SEND_MESSAGE("ERROR: coinlist.txt not exists.")
        return None
    with open(filePath, "r+") as txtFile:
        coinList = []
        for line in txtFile:
            line = line.strip()
            if line and not ("\t" in line): coinList.append(line)
        txtFile.seek(0)
        txtFile.truncate()
        for coin in coinList:
            txtFile.write(coin + "\n")
    txtFile.close()
    return coinList


def WRITE_CHANGELIST():
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"CHANGELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        coinList = READ_COINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        CALCULATE.SEND_MESSAGE(f"CHANGELIST File Updating (AVG: 3 Minutes)...")
        for coin in coinList:
            coin += "USDT"
            day = [0, 0, 0, 0, 0]
            for j in range(5): day[j] = CALCULATE.GET_CHANGE_PERCENT(coin, DEF.CHANGELIST_DAYS[j])
            avg = round((day[0] + day[1] + day[2] + day[3] + day[4]) / 5, 4)
            writer.writerow([coin, day[0], day[1], day[2], day[3], day[4], avg])
        CALCULATE.SEND_MESSAGE("CHANGELIST File Updated.")
    csvFile.close()
    return filePath


def READ_CHANGELIST():
    filePath = WRITE_CHANGELIST()
    with open(filePath, "r", newline="") as csvFile:
        headers = ["Coin_Symbol", "7D_Percent", "30D_Percent", "90D_Percent",
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
