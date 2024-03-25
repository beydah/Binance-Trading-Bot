# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
# MESSAGE
from src.engine.message import message as MSG
from src.engine.message import transactions as T
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def PATH(File_Name):
    if not LIB.OS.path.exists(DATA.Folder_Path): LIB.OS.makedirs(DATA.Folder_Path)
    return LIB.OS.path.join(DATA.Folder_Path, File_Name)
# ----------------------------------------------------------------


def CANDLE(Coin, Period=None, Limit=None, Datetime=None):
    candles = DATA.GET_CANDLE(Coin=Coin, Period=Period, Limit=Limit, Datetime=Datetime)
    path = PATH(f"{Coin}_{Period}.csv")
    with open(path, "w", newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        for candle in candles:
            candle[0] = LIB.DATE.datetime.fromtimestamp(candle[0] / 1000)
            candle[6] = LIB.DATE.datetime.fromtimestamp(candle[6] / 1000)
            writer.writerow(candle)
    return path
# ----------------------------------------------------------------


def WALLET():
    balances = DATA.GET_BALANCES()
    orders = READ.OPEN_ORDER()
    path = PATH("wallet.csv")
    with open(path, "w", newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        for balance in balances:
            if float(balance["free"]) <= 0: continue
            usdt_balance = CALCULATE.USDT_BALANCE(Coin=balance["asset"], Balance=float(balance["free"]))
            if usdt_balance <= DEF.Ignored_USDT_Balance: continue
            writer.writerow([balance["asset"], float(round(float(balance["free"]), 9)), float(round(usdt_balance, 3))])
        if orders is not None:
            for index, order in orders.iterrows():
                headers = [DEF.Wallet_Headers[0], DEF.Wallet_Headers[1], DEF.Wallet_Headers[2]]
                coin_info = [order[headers[0]], float(round(order[headers[1]], 9)), float(round(order[headers[2]], 3))]
                writer.writerow([coin_info[0], coin_info[1], coin_info[2]])
    return path


def WALLET_CHANGES():
    T.Transaction[T.Wallet] = True
    path = PATH("wallet_changes.csv")
    past_balances = []
    try:
        with open(path, "r", newline='') as file:
            reader = LIB.CSV.reader(file, delimiter=',')
            for row in reader: past_balances.append(float(row[0]))
    except Exception:
        with open(path, "w", newline=''): pass
    with open(path, "a", newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        total_usdt = CALCULATE.TOTAL_WALLET(0)
        changes = [0] * len(DEF.Wallet_Change_Days)
        for i in range(len(DEF.Wallet_Change_Days)):
            day = DEF.Wallet_Change_Days[i]
            changes[i] = DATA.FIND_WALLET_CHANGE(Now_Balance=total_usdt, Past_Balances=past_balances, Day=day)
        avg = round(sum(changes) / len(changes), 2)
        writer.writerow([total_usdt, changes[0], changes[1], changes[2], changes[3], changes[4], avg])
    T.Transaction[T.Wallet] = False
# ----------------------------------------------------------------


def COINLIST(Coins):
    T.Transaction[T.Coinlist] = True
    with open(LIB.OS.path.join(DATA.Folder_Path, "coinlist.txt"), 'w', newline='') as file: file.write(Coins)
    READ.OPTIMIZE_COINLIST()
    MSG.SEND("I Wrote Existing Coins")
    T.Transaction[T.Coinlist] = False


def INSERT_COINLIST(Coin):
    T.Transaction[T.Coinlist] = True
    if CALCULATE.FIND_COIN(Coin):
        with open(LIB.OS.path.join(DATA.Folder_Path, "coinlist.txt"), 'a', newline='') as file: file.write(Coin+"\n")
        MSG.SEND(f"I Insert {Coin}")
    T.Transaction[T.Coinlist] = False


def DROP_COINLIST(Coin):
    T.Transaction[T.Coinlist] = True
    coinlist = READ.COINLIST()
    if coinlist is None: MSG.SEND("I Don't Have Any Coin List\nPlease First 'Write Coin List'")
    else:
        dropped = False
        with open(LIB.OS.path.join(DATA.Folder_Path, "coinlist.txt"), 'w', newline='') as file:
            for coin in coinlist:
                if coin != Coin: file.write(coin+"\n")
                else: dropped = True
        if dropped: MSG.SEND(f"I Drop {Coin}")
        else: MSG.SEND(f"I Couldn't Find {Coin}")
    T.Transaction[T.Coinlist] = False


def COINLIST_CHANGES():
    T.Transaction[T.Coinlist] = True
    path = PATH("coinlist_changes.csv")
    coinlist = READ.COINLIST()
    if coinlist is None: MSG.SEND("I Don't Have Any Coin List\nPlease First 'Write Coin List'")
    else:
        MSG.SEND("Coinlist Changes Calculating...")
        with open(path, 'w', newline='') as file:
            writer = LIB.CSV.writer(file, delimiter=',')
            for coin in coinlist:
                changes = [0] * len(DEF.Coin_Change_Days)
                for i in range(5): changes[i] = CALCULATE.COIN_CHANGE(coin, DEF.Coin_Change_Days[i])
                avg = round(sum(changes) / len(changes), 2)
                writer.writerow([coin, changes[0], changes[1], changes[2], changes[3], changes[4], avg])
        MSG.SEND("Coinlist Changes Calculated.")
    T.Transaction[T.Coinlist] = False
# ----------------------------------------------------------------


def FAVORITELIST():
    path = PATH("favoritelist.csv")
    with open(path, 'w', newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        minlist = CALCULATE.MINLIST()
        for coin in minlist: writer.writerow([coin])


def DROP_FAVORITELIST(Coin):
    path = PATH("favoritelist.csv")
    coinlist = READ.FAVORITELIST()
    with open(path, 'w', newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        for coin in coinlist[DEF.Wallet_Headers[0]]:
            if coin != Coin: writer.writerow([coin])
# ----------------------------------------------------------------
