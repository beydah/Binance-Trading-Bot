# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
# MESSAGE
from src.engine.message import message as MESSAGE
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def PATH(FILENAME):
    if not LIB.OS.path.exists(DEF.DATA_FOLDER_PATH): LIB.OS.makedirs(DEF.DATA_FOLDER_PATH)
    return LIB.OS.path.join(DEF.DATA_FOLDER_PATH, FILENAME)
# ----------------------------------------------------------------


def CANDLE(SYMBOL, PERIOD, DATETIME=None, LIMIT=None):
    candles = DATA.GET_CANDLE(SYMBOL, PERIOD, DATETIME, LIMIT)
    filePath = PATH(f"{SYMBOL}_{PERIOD}.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for candle in candles:
            candle[0] = LIB.DATE.datetime.fromtimestamp(candle[0] / 1000)
            candle[6] = LIB.DATE.datetime.fromtimestamp(candle[6] / 1000)
            writer.writerow(candle)
    return filePath
# ----------------------------------------------------------------


def WALLET():
    balances = DATA.GET_BALANCES()
    orders = DATA.GET_OPEN_ORDER()
    filePath = PATH("WALLET.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for balance in balances:
            if float(balance["free"]) <= 0: continue
            USDTBalance = CALCULATE.USDT_BALANCE(balance["asset"], float(balance["free"]))
            if USDTBalance <= DEF.IGNORED_USDT_BALANCE: continue
            writer.writerow([balance["asset"], float(round(float(balance["free"]), 9)), float(round(USDTBalance, 3))])
        if orders is not None:
            for index, order in orders.iterrows():
                writer.writerow(
                    [order["Coin"], float(round(float(order["Quantity"]), 9)), float(round(order["USDT_Quantity"], 3))])
    return filePath


def WALLET_CHANGES():
    filePath = PATH("WALLET_CHANGES.csv")
    pastBalances = []
    try:
        with open(filePath, "r", newline='') as csvFile:
            reader = LIB.CSV.reader(csvFile, delimiter=',')
            for row in reader: pastBalances.append(float(row[0]))
    except Exception:
        with open(filePath, "w", newline=''): pass
    with open(filePath, "a", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        totalUSDT = CALCULATE.TOTAL_WALLET(0)
        percentChanges = [0] * len(DEF.WALLET_CHANGES_DAYS)
        for i in range(len(DEF.WALLET_CHANGES_DAYS)):
            percentChanges[i] = DATA.FIND_WALLET_CHANGE(totalUSDT, pastBalances, DEF.WALLET_CHANGES_DAYS[i])
        avg = round(sum(percentChanges) / len(percentChanges), 2)
        writer.writerow([totalUSDT, percentChanges[0], percentChanges[1], percentChanges[2],
                         percentChanges[3], percentChanges[4], avg])
# ----------------------------------------------------------------


def COINLIST(COINS):
    with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'w', newline='') as txtFile: txtFile.write(COINS)
    READ.OPTIMIZE_COINLIST()
    MESSAGE.SEND("I wrote the existing coins.")


def INSERT_COINLIST(COIN):
    try:
        with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'a', newline='') as txtFile:
            if not CALCULATE.FIND_COIN(COIN): return
            txtFile.write(COIN+"\n")
            MESSAGE.SEND("I insert the coin.")
    except Exception as e: MESSAGE.SEND_ERROR(f"INSERT_COINLIST: {e}")


def DROP_COINLIST(COIN):
    coinList = READ.COINLIST()
    if coinList is None: MESSAGE.SEND("I don't have any coin list.")
    if coinList is None or CALCULATE.FIND_COIN(COIN) is False: return
    with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'w', newline='') as txtFile:
        for coin in coinList:
            if coin != COIN: txtFile.write(coin+"\n")
            else: MESSAGE.SEND("I drop the coin.")


def COINLIST_CHANGES():
    filePath = PATH("COINLIST_CHANGES.csv")
    coinList = READ.COINLIST()
    if coinList is None: MESSAGE.SEND("I don't have any coin list.")
    else:
        with open(filePath, 'w', newline='') as csvFile:
            writer = LIB.CSV.writer(csvFile, delimiter=',')
            for coin in coinList:
                percentChanges = [0] * len(DEF.COIN_CHANGES_DAYS)
                for i in range(5): percentChanges[i] = CALCULATE.COIN_CHANGE(coin, DEF.COIN_CHANGES_DAYS[i])
                avg = round(sum(percentChanges) / len(percentChanges), 2)
                writer.writerow([coin, percentChanges[0], percentChanges[1], percentChanges[2],
                                 percentChanges[3], percentChanges[4], avg])
# ----------------------------------------------------------------


def FAVORITELIST():
    filePath = PATH("FAVORITELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        try:
            minList = DATA.FIND_MINLIST()
            for coin in minList: writer.writerow([coin])
        except Exception as e: MESSAGE.SEND_ERROR(f"FAVORITELIST: {e}")
# ----------------------------------------------------------------
