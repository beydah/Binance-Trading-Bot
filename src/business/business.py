# Added Pages
from src.settings import settings as S
from src.settings import api as API
from src.business import calculator as CALCULATE
# ----------------------------------------------------------------
# API Connections
CLIENT = S.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
TELEGRAM_BOT = S.BOT.TeleBot(API.TELEGRAM_BOT_KEY)
# ----------------------------------------------------------------


# Candle Transactions
def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    if CANDLE_LIMIT is None: CANDLE_LIMIT = S.CANDLE_LIMIT
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD,
                                              end_str=DATETIME, limit=CANDLE_LIMIT)
    if not S.OS.path.exists("../.data"): S.OS.makedirs("../.data")
    filePath = S.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = S.CSV.writer(csvFile, delimiter=',')
        for candleData in candleList:
            candleData[0] = S.TIME.fromtimestamp(candleData[0] / 1000)
            candleData[6] = S.TIME.fromtimestamp(candleData[6] / 1000)
            writer.writerow(candleData)
    csvFile.close()
    return filePath


def READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None, HEAD_ID=None):
    filePath = WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, CANDLE_LIMIT)
    with open(filePath, "r", newline='') as csvFile:
        headers = ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
                   "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = S.PD.read_csv(filePath, names=headers)
    csvFile.close()
    if HEAD_ID is None: return df
    elif -1 < HEAD_ID < 12: return df[headers[HEAD_ID]]


def DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    filePath = S.OS.path.join("../.data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    if S.OS.path.exists(filePath): S.OS.remove(filePath)
# ----------------------------------------------------------------


# Change Transactions
def READ_COINLIST():
    filePath = S.OS.path.join("settings", "coinlist.csv")
    with open(filePath, "r", newline='') as csvFile:
        headers = ["Coin_Name"]
        df = S.PD.read_csv(filePath, names=headers)
        df = df.apply(lambda x: x.str.strip())
        df = df.dropna()
    csvFile.close()
    return df[headers[0]]


def WRITE_CHANGELIST():
    if not S.OS.path.exists("../.data"): S.OS.makedirs("../.data")
    filePath = S.OS.path.join("../.data", f"CHANGELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        coinList = READ_COINLIST()
        writer = S.CSV.writer(csvFile, delimiter=',')
        SEND_MESSAGE(f"CHANGELIST File Updating...")
        for i in range(len(coinList)):
            coinSymbol = coinList[i] + "USDT"
            day = [0, 0, 0, 0, 0, 0]
            for j in range(6): day[j] = CALCULATE.CHANGE_PERCENT(coinSymbol, S.CHANGELIST_DAYS[j])
            avg = round((day[0] + day[1] + day[2] + day[3] + day[4] + day[5]) / 6, 4)
            writer.writerow([coinSymbol, day[0], day[1], day[2], day[3], day[4], day[5], avg])
        SEND_MESSAGE("CHANGELIST File Updated.")
    csvFile.close()
    return filePath


def READ_CHANGELIST():
    filePath = WRITE_CHANGELIST()
    with open(filePath, "r", newline="") as csvFile:
        headers = ["Coin_Symbol", "1D_Percent", "7D_Percent", "30D_Percent", "90D_Percent",
                   "180D_Percent", "365D_Percent", "AVG_Percent"]
        df = S.PD.read_csv(filePath, names=headers)
    csvFile.close()
    return df


def WRITE_FAVORITECOINS():
    if not S.OS.path.exists("../.data"): S.OS.makedirs("../.data")
    filePath = S.OS.path.join("../.data", f"FAVORITECOINS.csv")
    with open(filePath, 'w', newline='') as csvFile:
        minimumCoinList = CALCULATE.FIND_MINIMUMLIST()
        writer = S.CSV.writer(csvFile, delimiter=',')
        for coin in minimumCoinList: writer.writerow([coin])
    csvFile.close()
# ----------------------------------------------------------------


# Telegram Transactions
def SEND_MESSAGE(BOT_MESSAGE):
    URL = (f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
           f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
           f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    S.REQUEST.get(URL)
# ----------------------------------------------------------------


# Other Transactions
def GET_SYMBOL_FROM_ID(SYMBOL_ID):
    filePath = S.OS.path.join("../.data", f"FAVORITECOINS.csv")
    if S.OS.path.exists(filePath) is False: WRITE_FAVORITECOINS()
    with open(filePath, "r", newline="") as csvFile:
        headers = ["Coin_Symbol"]
        df = S.PD.read_csv(filePath, names=headers)
    csvFile.close()
    favorite_coins = df["Coin_Symbol"].tolist()
    return favorite_coins[SYMBOL_ID]


def GET_PERIOD_FROM_ID(PERIOD_ID): return S.CANDLE_PEROIDS[PERIOD_ID]
# ----------------------------------------------------------------
