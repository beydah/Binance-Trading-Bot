# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
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


def NEW_PATH(FILENAME):
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    return LIB.OS.path.join("../.data", FILENAME)
# ----------------------------------------------------------------


def CANDLE(COIN, CANDLE_PERIOD, DATETIME=None, CANDLE_LIMIT=None):
    candles = DATA.GET_CANDLE(COIN, CANDLE_PERIOD, DATETIME, CANDLE_LIMIT)
    filePath = NEW_PATH(f"{COIN}_{CANDLE_PERIOD}.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for candle in candles:
            candle[0] = LIB.DATE.datetime.fromtimestamp(candle[0] / 1000)
            candle[6] = LIB.DATE.datetime.fromtimestamp(candle[6] / 1000)
            writer.writerow(candle)
    return filePath
# ----------------------------------------------------------------


def WALLET():
    filePath = NEW_PATH("WALLET.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        balances = DATA.GET_BALANCES()
        for balance in balances:
            if float(balance["free"]) > 0:
                USDTBalance = DATA.GET_USDT_BALANCE(balance["asset"], float(balance["free"]))
                if USDTBalance > 1: writer.writerow([balance["asset"], balance["free"], USDTBalance])
    return filePath


def WALLET_CHANGES():
    filePath = NEW_PATH("WALLET_CHANGES.csv")
    pastBalances = []
    try:
        with open(filePath, "r", newline='') as csvFile:
            reader = LIB.CSV.reader(csvFile, delimiter=',')
            for row in reader: pastBalances.append(float(row[0]))
    except Exception:
        with open(filePath, "w", newline=''): pass
    with open(filePath, "a", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        days = [1, 3, 7, 15, 30]
        percentChanges = [0, 0, 0, 0, 0]
        totalUSDT = DATA.GET_TOTAL_WALLET(0)
        for i in range(5): percentChanges[i] = DATA.GET_WALLET_CHANGE(totalUSDT, pastBalances, days[i])
        avg = round((percentChanges[0] + percentChanges[1] + percentChanges[2] +
                     percentChanges[3] + percentChanges[4]) / 5, 2)
        writer.writerow([totalUSDT, percentChanges[0], percentChanges[1],
                         percentChanges[2], percentChanges[3], percentChanges[4], avg])
# ----------------------------------------------------------------


def COINLIST(COINS):
    with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'w', newline='') as txtFile: txtFile.write(COINS)
    READ.COINLIST()


def COINLIST_CHANGES():
    filePath = NEW_PATH("COINLIST_CHANGES.csv")
    with open(filePath, 'w', newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        coinList = READ.COINLIST()
        if coinList is not None:
            changeListDays = [7, 30, 90, 180, 365]
            for coin in coinList:
                if DATA.FIND_COIN(coin):
                    day = [0, 0, 0, 0, 0]
                    for i in range(5): day[i] = DATA.GET_COIN_CHANGE(coin, changeListDays[i])
                    avg = round((day[0] + day[1] + day[2] + day[3] + day[4]) / 5, 4)
                    writer.writerow([coin, day[0], day[1], day[2], day[3], day[4], avg])
# ----------------------------------------------------------------


def FAVORITELIST():
    filePath = NEW_PATH("FAVORITELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        minList = DATA.FIND_MINLIST()
        for coin in minList: writer.writerow([coin])
# ----------------------------------------------------------------
