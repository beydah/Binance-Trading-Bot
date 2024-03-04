# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
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


# List Operations
def WRITE_COIN(COINLIST):
    if not LIB.OS.path.exists("settings"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("settings", "coinlist.txt")
    with open(filePath, 'w', newline='') as txtFile: txtFile.write(COINLIST)


def READ_COIN():
    filePath = LIB.OS.path.join("settings", "coinlist.txt")
    if not LIB.OS.path.exists(filePath):
        MESSAGE.SEND("I couldn't find the coin list. Please first write the 'Write Coin List' "
                     "command and enter the command.")
        return None
    with open(filePath, "r+") as txtFile:
        coinList = []
        for line in txtFile:
            line = line.strip().upper()
            if line and not ("\t" in line): coinList.append(line)
        txtFile.seek(0)
        txtFile.truncate()
        for coin in coinList: txtFile.write(coin + "\n")
    return coinList


def WRITE_FULLCOIN():
    while True:
        try:
            binance = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
            account = binance.get_account(timestamp=LIB.TIME() - 1000)
            balances = account["balances"]
            break
        except Exception:
            MESSAGE.SEND(f"Error: {Exception}")
            LIB.SLEEP(15)
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"FULLCOINLIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for balance in balances: writer.writerow([balance["asset"]])


def READ_FULLCOIN():
    filePath = LIB.OS.path.join("../.data", f"FULLCOINLIST.csv")
    if not LIB.OS.path.exists(filePath): WRITE_FULLCOIN()
    with open(filePath, "r", newline=''):
        headers = ["Coin"]
        df = LIB.PD.read_csv(filePath, names=headers)
    return df


def WRITE_CHANGE():
    changeListDays = [7, 30, 90, 180, 365]
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"CHANGELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        coinList = READ_COIN()
        MESSAGE.SEND("Coin Change List is Updating...\n(Average 3 Minutes)")
        for coin in coinList:
            found = CALCULATE.FIND_COIN(coin)
            if not found: continue
            coinSymbol = coin + "USDT"
            day = [0, 0, 0, 0, 0]
            for j in range(5): day[j] = CALCULATE.GET_CHANGE_COIN(coinSymbol, changeListDays[j])
            avg = round((day[0] + day[1] + day[2] + day[3] + day[4]) / 5, 4)
            writer.writerow([coin, day[0], day[1], day[2], day[3], day[4], avg])
        MESSAGE.SEND("Coin Change List is Updated.")


def READ_CHANGE():
    filePath = LIB.OS.path.join("../.data", f"CHANGELIST.csv")
    if not LIB.OS.path.exists(filePath): WRITE_CHANGE()
    with open(filePath, "r", newline=""):
        headers = ["Coin_Symbol", "7D_Percent", "30D_Percent", "90D_Percent",
                   "180D_Percent", "365D_Percent", "AVG_Percent"]
        df = LIB.PD.read_csv(filePath, names=headers)
    return df


def WRITE_FAVORITE():
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        MESSAGE.SEND(f"FAVORITELIST File Updating...")
        WRITE_CHANGE()
        minimumCoinList = CALCULATE.GET_MINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for coin in minimumCoinList: writer.writerow([coin])
        MESSAGE.SEND(f"FAVORITELIST File Updated.")
# ----------------------------------------------------------------
