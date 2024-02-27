# ----------------------------------------------------------------
# Added Links
from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
from src.engine import calculator as CALCULATE
# ----------------------------------------------------------------
# API Connections
BINANCE = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
# TELEGRAM_BOT = LIB.BOT.TeleBot(API.TELEGRAM_BOT_KEY)
# ----------------------------------------------------------------


# Candle CRUDs
def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    if CANDLE_LIMIT is None: CANDLE_LIMIT = DEF.CANDLE_LIMIT
    if DATETIME is None:
        DATETIME = LIB.DATETIME.now()
        DATETIME = DATETIME.strftime("%Y-%m-%d %H:%M:%S")
    while True:
        try:
            candleList = BINANCE.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD,
                                                       end_str=DATETIME, limit=CANDLE_LIMIT)
            break
        except Exception as e:
            CALCULATE.MESSAGE(f"Error: {e}")
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


def READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None, HEAD_ID=None):
    filePath = WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, CANDLE_LIMIT)
    with open(filePath, "r", newline=''):
        headers = ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
                   "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = LIB.PD.read_csv(filePath, names=headers)
    DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    if HEAD_ID is None: return df
    elif HEAD_ID > -1 and HEAD_ID < 12: return df[headers[HEAD_ID]]


def DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    try:
        filePath = LIB.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
        if LIB.OS.path.exists(filePath): LIB.OS.remove(filePath)
    except Exception: pass
# ----------------------------------------------------------------


# Wallet CRUDs
def WRITE_WALLET():
    while True:
        try:
            account = BINANCE.get_account(timestamp=LIB.TIME()-1000)
            balances = account["balances"]
            break
        except Exception as e:
            CALCULATE.MESSAGE(f"Error: {e}")
            LIB.SLEEP(15)
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", "WALLET.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for balance in balances:
            if float(balance["free"]) > 0:
                USDTBalance = CALCULATE.FIND_USDT_BALANCE(balance["asset"], float(balance["free"]))
                writer.writerow([balance["asset"], balance["free"], USDTBalance])
    return filePath


def READ_WALLET(COIN=None, HEAD_ID=None):
    filePath = WRITE_WALLET()
    with open(filePath, "r", newline='') as csvFile:
        headers = ["Coin", "Balance", "UDST_Balance"]
        df = LIB.PD.read_csv(filePath, names=headers)
    if COIN is None and HEAD_ID is None: return df
    elif COIN is not None and HEAD_ID is None: return df[df["Coin"] == COIN]  # .values[0]
    elif COIN is None and HEAD_ID is not None: return df[headers[HEAD_ID]]
    return df[df["Coin"] == COIN][headers[HEAD_ID]]
# ----------------------------------------------------------------


# Change CRUDs
def READ_COINLIST():
    filePath = LIB.OS.path.join("settings", "coinlist.txt")
    if not LIB.OS.path.exists(filePath):
        CALCULATE.MESSAGE("ERROR: coinlist.txt not exists.")
        return None
    with open(filePath, "r+") as txtFile:
        coinList = []
        for line in txtFile:
            line = line.strip()
            if line and not ("\t" in line): coinList.append(line)
        txtFile.seek(0)
        txtFile.truncate()
        for coin in coinList: txtFile.write(coin + "\n")
    return coinList


def WRITE_CHANGELIST():
    changeListDays = [7, 30, 90, 180, 365]
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"CHANGELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        coinList = READ_COINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        CALCULATE.MESSAGE(f"CHANGELIST File Updating (AVG: 3 Minutes)...")
        # Git ve ACCOUNT içindenki balance değerinde olan tüm coinlerin isimlerini çek
        for coin in coinList:
            # Çektiğin coin isimlerinde şuanki coin ismini oku
            # eğer okuma sırasında coini bulamazsan bulunmadı mesajı gönder ve bu coini kullanma
            coinSymbol = coin + "USDT"
            day = [0, 0, 0, 0, 0]
            for j in range(5): day[j] = CALCULATE.GET_CHANGE_PERCENT(coinSymbol, changeListDays[j])
            avg = round((day[0] + day[1] + day[2] + day[3] + day[4]) / 5, 4)
            writer.writerow([coin, day[0], day[1], day[2], day[3], day[4], avg])
        CALCULATE.MESSAGE("CHANGELIST File Updated.")
    return filePath


def READ_CHANGELIST():
    filePath = WRITE_CHANGELIST()
    with open(filePath, "r", newline=""):
        headers = ["Coin_Symbol", "7D_Percent", "30D_Percent", "90D_Percent",
                   "180D_Percent", "365D_Percent", "AVG_Percent"]
        df = LIB.PD.read_csv(filePath, names=headers)
    return df


def WRITE_FAVORITELIST():
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        CALCULATE.MESSAGE(f"FAVORITELIST File Updating...")
        minimumCoinList = CALCULATE.GET_MINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for coin in minimumCoinList: writer.writerow([coin])
        CALCULATE.MESSAGE(f"FAVORITELIST File Updated.")
# ----------------------------------------------------------------
