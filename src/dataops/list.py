# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import algotest as TEST
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# List Operations
def READ_COIN():
    filePath = LIB.OS.path.join("settings", "coinlist.txt")
    if not LIB.OS.path.exists(filePath): LIB.OS.makedirs(filePath)
    with open(filePath, "r+") as txtFile:
        coinList = []
        for line in txtFile:
            line = line.strip()
            if line and not ("\t" in line): coinList.append(line)
        txtFile.seek(0)
        txtFile.truncate()
        for coin in coinList: txtFile.write(coin + "\n")
    return coinList


def WRITE_CHANGE():
    changeListDays = [7, 30, 90, 180, 365]
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", f"CHANGELIST.csv")
    with open(filePath, 'w', newline='') as csvFile:
        coinList = READ_COIN()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        MESSAGE.SEND(f"CHANGELIST File Updating (AVG: 3 Minutes)...")
        # TODO: Account icindeki balance degerinde olan tum coinlerin ismini al = fullCoinList
        for coin in coinList:
            # TODO: Eger coin fullCoinList icinde yoksa hata gonder ve bu coini gec
            coinSymbol = coin + "USDT"
            day = [0, 0, 0, 0, 0]
            for j in range(5): day[j] = CALCULATE.GET_CHANGE_PERCENT(coinSymbol, changeListDays[j])
            avg = round((day[0] + day[1] + day[2] + day[3] + day[4]) / 5, 4)
            writer.writerow([coin, day[0], day[1], day[2], day[3], day[4], avg])
        MESSAGE.SEND("CHANGELIST File Updated.")
    return filePath


def READ_CHANGE():
    filePath = WRITE_CHANGE()
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
        minimumCoinList = CALCULATE.GET_MINLIST()
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for coin in minimumCoinList: writer.writerow([coin])
        MESSAGE.SEND(f"FAVORITELIST File Updated.")
# ----------------------------------------------------------------
