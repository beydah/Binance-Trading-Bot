# Added Pages
from src.settings import settings as S
from src.settings import api as API
# ----------------------------------------------------------------

# API Connections
CLIENT = S.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
TELEGRAM_BOT = S.BOT.TeleBot(API.TELEGRAM_BOT_KEY)
# ----------------------------------------------------------------


# Candle Transactions
def GET_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD,
                                              end_str=DATETIME, limit=S.CANDLE_LIMIT)
    return candleList


def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    if not S.OS.path.exists("../data"): S.OS.makedirs("../data")
    folderPath = S.OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(folderPath, "w", newline='') as csvFile:
        writer = S.CSV.writer(csvFile, delimiter=',')
        for candleData in GET_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME):
            candleData[0] = S.TIME.fromtimestamp(candleData[0] / 1000)
            candleData[6] = S.TIME.fromtimestamp(candleData[6] / 1000)
            writer.writerow(candleData)
    csvFile.close()


def READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, HEAD_ID=None):
    WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME)
    readCSV = S.OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(readCSV, "r", newline='') as csvFile:
        headers = \
            ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
             "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = S.PD.read_csv(readCSV, names=headers)
    csvFile.close()
    if HEAD_ID is None:
        return df
    elif -1 < HEAD_ID < 12:
        header = headers[HEAD_ID]
        return df[header]
    else:
        return "Unknown HEAD_ID"
# ----------------------------------------------------------------


# Telegram Transactions
def SEND_MESSAGE(BOT_MESSAGE):
    URL = \
        (f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
         f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
         f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    S.REQUEST.get(URL)
# ----------------------------------------------------------------


# Other Transactions
def COMBINE_SYMBOL(LEFT_SYMBOL, RIGHT_SYMBOL):
    combinerSymbol = LEFT_SYMBOL + RIGHT_SYMBOL
    return combinerSymbol


def GET_SYMBOL_FROM_ID(SYMBOL_ID):
    coinSymbol = S.COIN_SYMBOLS[SYMBOL_ID]
    return coinSymbol


def GET_PERIOD_FROM_ID(PERIOD_ID):
    candlePeriod = S.CANDLE_PEROIDS[PERIOD_ID]
    return candlePeriod
# ----------------------------------------------------------------
