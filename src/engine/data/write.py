# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
# MESSAGE
from src.engine.message import message as MSG
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def PATH(File_Name):
    if not LIB.OS.path.exists(DATA.Folder_Path): LIB.OS.makedirs(DATA.Folder_Path)
    return LIB.OS.path.join(DATA.Folder_Path, File_Name)
# ----------------------------------------------------------------


def CANDLE(Coin, Period=None, Datetime=None, Limit=None):
    candles = DATA.GET_CANDLE(Coin, Period, Datetime, Limit)
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
    path = PATH("WALLET.csv")
    with open(path, "w", newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        for balance in balances:
            if float(balance["free"]) <= 0: continue
            usdt_balance = CALCULATE.USDT_BALANCE(balance["asset"], float(balance["free"]))
            if usdt_balance <= DEF.Ignored_USDT_Balance: continue
            writer.writerow([balance["asset"], float(round(float(balance["free"]), 9)), float(round(usdt_balance, 3))])
        if orders is not None:
            for index, order in orders.iterrows():
                writer.writerow(
                    [order["Coin"], float(round(float(order["Balance"]), 9)), float(round(order["USDT Balance"], 3))])
    return path


def WALLET_CHANGES():
    path = PATH("WALLET_CHANGES.csv")
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
        percent_changes = [0] * len(DEF.Wallet_Change_Days)
        for i in range(len(DEF.Wallet_Change_Days)):
            percent_changes[i] = DATA.FIND_WALLET_CHANGE(total_usdt, past_balances, DEF.Wallet_Change_Days[i])
        avg = round(sum(percent_changes) / len(percent_changes), 2)
        writer.writerow([total_usdt, percent_changes[0], percent_changes[1], percent_changes[2],
                         percent_changes[3], percent_changes[4], avg])
# ----------------------------------------------------------------


def COINLIST(Coins):
    with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'w', newline='') as file: file.write(Coins)
    READ.OPTIMIZE_COINLIST()
    MSG.SEND("I Wrote Existing Coins")
    COINLIST_CHANGES()
    FAVORITELIST()


def INSERT_COINLIST(Coin):
    if not CALCULATE.FIND_COIN(Coin): return
    with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'a', newline='') as file: file.write(Coin+"\n")
    MSG.SEND(f"I Insert {Coin}")


def DROP_COINLIST(Coin):
    coinlist = READ.COINLIST()
    if coinlist is None: MSG.SEND("I Don't Have Any Coin List\nPlease First 'Write Coin List'")
    else:
        dropped = False
        with open(LIB.OS.path.join("engine/settings", "coinlist.txt"), 'w', newline='') as file:
            for coin in coinlist:
                if coin != Coin: file.write(coin+"\n")
                else: dropped = True
        if dropped: MSG.SEND(f"I Drop {Coin}")
        else: MSG.SEND(f"I Couldn't Find {Coin}")


def COINLIST_CHANGES():
    path = PATH("COINLIST_CHANGES.csv")
    coinlist = READ.COINLIST()
    if coinlist is None: MSG.SEND("I Don't Have Any Coin List\nPlease First 'Write Coin List'")
    else:
        MSG.SEND("Coinlist Changes Calculating...")
        with open(path, 'w', newline='') as file:
            writer = LIB.CSV.writer(file, delimiter=',')
            for coin in coinlist:
                percent_changes = [0] * len(DEF.Coin_Change_Days)
                for i in range(5): percent_changes[i] = CALCULATE.COIN_CHANGE(coin, DEF.Coin_Change_Days[i])
                avg = round(sum(percent_changes) / len(percent_changes), 2)
                writer.writerow([coin, percent_changes[0], percent_changes[1], percent_changes[2],
                                 percent_changes[3], percent_changes[4], avg])
        MSG.SEND("Coinlist Changes Calculated.")
# ----------------------------------------------------------------


def FAVORITELIST():
    path = PATH("FAVORITELIST.csv")
    with open(path, 'w', newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        minlist = DATA.FIND_MINLIST()
        for coin in minlist: writer.writerow([coin])


def DROP_FAVORITELIST(Coin):
    path = PATH("FAVORITELIST.csv")
    coinlist = READ.FAVORITELIST()
    with open(path, 'w', newline='') as file:
        writer = LIB.CSV.writer(file, delimiter=',')
        for coin in coinlist["Coin"]:
            if coin != Coin: writer.writerow([coin])
            else: MSG.SEND(f"I Drop {Coin} in Favorite List")
# ----------------------------------------------------------------
