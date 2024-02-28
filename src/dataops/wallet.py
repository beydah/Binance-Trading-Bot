# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE

from src.engine import algotest as TEST
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

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
            MESSAGE.SEND(f"Error: {Exception}")
            LIB.SLEEP(15)
    if not LIB.OS.path.exists("../.data"): LIB.OS.makedirs("../.data")
    filePath = LIB.OS.path.join("../.data", "WALLET.csv")
    with open(filePath, "w", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        for balance in balances:
            if float(balance["free"]) > 0:
                USDTBalance = CALCULATE.FIND_USDT_BALANCE(balance["asset"], float(balance["free"]))
                if USDTBalance > 0.01: writer.writerow([balance["asset"], balance["free"], round(USDTBalance, 2)])
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
        for row in reader: pastBalances.append(float(row[0]))
    with open(filePath, "a", newline='') as csvFile:
        writer = LIB.CSV.writer(csvFile, delimiter=',')
        try:
            percentChange = (totalBalance - pastBalances[-1]) / pastBalances[-1] * 100
            avgTotalBalance = sum(pastBalances) / len(pastBalances)
            avgPercentChange = (totalBalance - avgTotalBalance) / avgTotalBalance * 100
            writer.writerow([totalBalance, round(percentChange, 2), round(avgPercentChange, 2)])
        except Exception:
            print(Exception)
            writer.writerow([totalBalance, 0, 0])
    return filePath
# ----------------------------------------------------------------
