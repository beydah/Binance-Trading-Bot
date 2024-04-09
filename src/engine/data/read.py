# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
# MATH
from src.engine.trade import calculator as CALCULATE
# MESSAGE
from src.engine.bot import message as MSG
from src.engine.bot import transactions as T
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def CANDLE(Coin, Period=None, Limit=None, Datetime=None, Head_ID=None):
    path = WRITE.CANDLE(Coin=Coin, Period=Period, Limit=Limit, Datetime=Datetime)
    with open(path, "r", newline=''): df = LIB.PD.read_csv(path, names=DEF.Candle_Headers)
    LIB.OS.remove(path)
    if Head_ID is None: return df
    return df[DEF.Candle_Headers[Head_ID]]
# ----------------------------------------------------------------


def WALLET(Coin=None, Head_ID=None):
    path = WRITE.WALLET()
    with open(path, "r", newline=''): df = LIB.PD.read_csv(path, names=DEF.Wallet_Headers)
    if Coin is None and Head_ID is None: return df
    elif Coin is not None and Head_ID is None: return df[df[DEF.Wallet_Headers[0]] == Coin]
    elif Coin is None and Head_ID is not None: return df[DEF.Wallet_Headers[Head_ID]]
    return df[df[DEF.Wallet_Headers[0]] == Coin][DEF.Wallet_Headers[Head_ID]]


def WALLET_CHANGES(Head_ID=None):
    path = LIB.OS.path.join(DATA.Folder_Path, "wallet_changes.csv")
    if not LIB.OS.path.exists(path): WRITE.WALLET_CHANGES()
    try:
        with open(path, "r", newline=''): df = LIB.PD.read_csv(path, names=DEF.Wallet_Changes_Headers)
        if Head_ID is None: return df.tail(1)
        return df[DEF.Wallet_Changes_Headers[Head_ID]].tail(1)
    except Exception as e: MSG.SEND_ERROR(f"WALLET_CHANGES: {e}")
# ----------------------------------------------------------------


def OPEN_ORDER():
    open_orders = DATA.GET_OPEN_ORDERS()
    if open_orders is None: return None
    orders = []
    for order in open_orders:
        coin = order['symbol'].removesuffix("USDT")
        quantity = float(order['origQty'])
        close_price = CANDLE(Coin=coin, Period="1m", Limit=1, Head_ID=4)
        usdt_quantity = float(DATA.FIND_USDT_QUANTITY(Coin_Quantity=quantity, Coin_Price=close_price[0]))
        headers = [DEF.Wallet_Headers[0], DEF.Wallet_Headers[1], DEF.Wallet_Headers[2]]
        orders.append({headers[0]: coin, headers[1]: quantity, headers[2]: usdt_quantity})
    return LIB.PD.DataFrame(orders)
# ----------------------------------------------------------------


def COINLIST():
    try:
        OPTIMIZE_COINLIST()
        coinlist = []
        with open(LIB.OS.path.join(DATA.Folder_Path, "coinlist.txt"), "r+") as file:
            for line in file: coinlist.append(line.strip())
        return coinlist
    except Exception as e: MSG.SEND_ERROR(f"COINLIST: {e}")


def OPTIMIZE_COINLIST():
    T.Transaction[T.Coinlist] = True
    try:
        with open(LIB.OS.path.join(DATA.Folder_Path, "coinlist.txt"), "r+") as file:
            coinlist = []
            for line in file:
                line = line.strip().upper()
                if line and not ("\t" in line):
                    if CALCULATE.FIND_COIN(line): coinlist.append(line)
            file.seek(0)
            file.truncate()
            for coin in coinlist: file.write(coin+"\n")
    except Exception as e: MSG.SEND_ERROR(f"OPTIMIZE_COINLIST: {e}")
    T.Transaction[T.Coinlist] = False


def COINLIST_CHANGES():
    path = LIB.OS.path.join(DATA.Folder_Path, "coinlist_changes.csv")
    if not LIB.OS.path.exists(path): WRITE.COINLIST_CHANGES()
    try:
        with open(path, "r", newline=""): return LIB.PD.read_csv(path, names=DEF.Coinlist_Changes_Headers)
    except Exception as e: MSG.SEND_ERROR(f"COINLIST_CHANGES: {e}")
# ----------------------------------------------------------------


def FAVORITELIST():
    path = LIB.OS.path.join(DATA.Folder_Path, f"favoritelist.csv")
    if not LIB.OS.path.exists(path): WRITE.FAVORITELIST()
    try:
        with open(path, "r", newline=''): return LIB.PD.read_csv(path, names=[DEF.Wallet_Headers[0]])
    except Exception as e: MSG.SEND_ERROR(f"FAVORITELIST: {e}")
# ----------------------------------------------------------------
