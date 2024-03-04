# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE

from src.engine import algorithm as ALGORITHM
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL
from src.engine import analysis as ANALYSIS

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Wallet Operations
def WRITE():
    while True:
        try:
            binance = LIB.BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
            account = binance.get_account(timestamp=LIB.TIME()-1000)
            balances = account["balances"]
            break
        except Exception:
            MESSAGE.SEND(f"Error5555: {Exception}")
            LIB.SLEEP(15)
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", "WALLET.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for balance in balances:
            if float(balance["free"]) > 0:
                USDTBalance = CALCULATE.FIND_USDT_BALANCE(balance["asset"], float(balance["free"]))
                if USDTBalance > 1: writer.writerow([balance["asset"], balance["free"], round(USDTBalance, 2)])
    return filePath


def READ(COIN=None, HEAD_ID=None):
    filePath = WRITE()
    with open(filePath, "r", newline=''):
        headers = ["Coin", "Balance", "USDT_Balance"]
        df = LIB.PD.read_csv(filePath, names=headers)
    if COIN is None and HEAD_ID is None: return df
    elif COIN is not None and HEAD_ID is None: return df[df["Coin"] == COIN]
    elif COIN is None and HEAD_ID is not None: return df[headers[HEAD_ID]]
    return df[df["Coin"] == COIN][headers[HEAD_ID]]


def WRITE_TOTAL_BALANCE():
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", "TOTAL_BALANCE.csv")
    if not LIB.OS.path.exists(filePath):
        with open(filePath, "w", newline=''): pass
    totalBalance = CALCULATE.TOTAL_WALLET()
    pastBalances = []
    with open(filePath, "r", newline='') as csvFile:
        reader = LIB.CSV.reader(csvFile, delimiter=',')
        try:
            for row in reader: pastBalances.append(float(row[0]))
        except Exception:
            with open(filePath, "w", newline=''): pass
    with open(filePath, "a", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        days = [1, 3, 7, 15, 30]
        percentChanges = [0, 0, 0, 0, 0]
        for i in range(5):
            percentChanges[i] = CALCULATE.GET_CHANGE_WALLET(totalBalance, pastBalances, days[i])
        writer.writerow([totalBalance, percentChanges[0], percentChanges[1],
                         percentChanges[2], percentChanges[3], percentChanges[4]])


def READ_TOTAL_BALANCE(HEAD_ID=None):
    filePath = LIB.OS.path.join("../.data", "TOTAL_BALANCE.csv")
    if not LIB.OS.path.exists(filePath): WRITE_TOTAL_BALANCE()
    with open(filePath, "r", newline=''):
        headers = ["Total_Balance", "1Day_Change", "3Day_Change",
                   "7Day_Change", "15Day_Change", "30Day_Change"]
        df = LIB.PD.read_csv(filePath, names=headers)
    if HEAD_ID is None: return df.tail(1)
    elif HEAD_ID > -1 and HEAD_ID < 6: return df[headers[HEAD_ID]].tail(1)

# ----------------------------------------------------------------
