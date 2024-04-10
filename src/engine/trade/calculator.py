# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.trade import indicator as INDICATOR
# MESSAGE
from src.engine.bot import message as MSG
from src.engine.bot import transactions as T
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def MARKET_BUY(Coin, Quantity):
    virtual_quantity = VIRTUAL_QUANTITY(Transaction="Market Buy", Coin=Coin, Quantity=LIB.DECIMAL(Quantity))
    if virtual_quantity is None: return False
    binance = DATA.GET_BINANCE()
    while True:
        try:
            binance.order_market(symbol=Coin+"USDT", side="BUY", quantity=virtual_quantity)
            break
        except Exception as e: MSG.SEND_ERROR(f"MARKET_BUY: {e}")
    MSG.SEND(f"Buy - {virtual_quantity} {Coin}")
    return True


def MARKET_SELL(Coin, Quantity):
    virtual_quantity = VIRTUAL_QUANTITY(Transaction="Market Sell", Coin=Coin, Quantity=LIB.DECIMAL(Quantity))
    if virtual_quantity is None: return False
    binance = DATA.GET_BINANCE()
    while True:
        try:
            binance.order_market(symbol=Coin+"USDT", side="SELL", quantity=virtual_quantity)
            break
        except Exception as e: MSG.SEND_ERROR(f"MARKET_SELL: {e}")
    MSG.SEND(f"Sell - {virtual_quantity} {Coin}")
    return True


def STOP_LOSS(Coin):
    balance = READ.WALLET(Coin=Coin, Head_ID=1)
    virtual_quantity = VIRTUAL_QUANTITY(Transaction="Stop Loss", Coin=Coin, Quantity=LIB.DECIMAL(balance.item()))
    if virtual_quantity is None: return False
    binance = DATA.GET_BINANCE()
    while True:
        try:
            price = READ.CANDLE(Coin=Coin, Period="1m", Limit=1, Head_ID=4)
            stop_price = round(float(price[0]) * DEF.Stop_Loss_Rate, len(str(price[0]).split(".")[-1]))
            binance.create_order(symbol=Coin+"USDT", type="STOP_LOSS_LIMIT", side="SELL",
                                 price=stop_price, stopPrice=stop_price, quantity=virtual_quantity, timeInForce="GTC")
            break
        except Exception as e: MSG.SEND_ERROR(f"STOP_LOSS: {e}")
    MSG.SEND(f"Buy Price: {float(price[0])}\nStop Loss Price: {float(stop_price)}\n")
    return True


def DELETE_STOP_LOSS(Coin):
    binance = DATA.GET_BINANCE()
    while True:
        try:
            order_id = DATA.GET_STOP_LOSS_ORDER(Coin)
            if order_id is None: return False
            order_id = order_id['orderId']
            binance.cancel_order(symbol=Coin+"USDT", orderId=order_id)
            return True
        except Exception as e: MSG.SEND_ERROR(f"DELETE_STOP_LOSS: {e}")


def TEST_BUY(USDT_Quantity, Coin_Price):
    return DEF.Binance_Comission_Rate * DATA.FIND_COIN_QUANTITY(USDT_Quantity=USDT_Quantity, Coin_Price=Coin_Price)


def TEST_SELL(Coin_Quantity, Coin_Price):
    return DEF.Binance_Comission_Rate * DATA.FIND_USDT_QUANTITY(Coin_Quantity=Coin_Quantity, Coin_Price=Coin_Price)
# ----------------------------------------------------------------


def VIRTUAL_QUANTITY(Transaction, Coin, Quantity):
    quantity_info = [DATA.GET_SYMBOL_INFO(Coin=Coin, Info="minQty"), DATA.GET_SYMBOL_INFO(Coin=Coin, Info="maxQty")]
    if LIB.DECIMAL(quantity_info[0]) > Quantity:
        MSG.SEND(f"I can't {Transaction} {Coin}\nBeacuse Min Quantity: {float(quantity_info[0])}\n"
                 f"My Request Quantity: {float(Quantity)}\n")
        return None
    if LIB.DECIMAL(quantity_info[1]) < Quantity: Quantity = LIB.DECIMAL(quantity_info[1])
    min_step = 0
    for char in quantity_info[0]:
        if char == "0": min_step += 1
        elif char == "1": break
    if Quantity == int(Quantity): virtual_quantity = f"{int(Quantity)}."+("0" * 8)
    else: virtual_quantity = str(LIB.DECIMAL(Quantity))
    left_str, right_str = virtual_quantity.split(".")
    right_str = right_str[:min_step]
    if right_str == "": return left_str
    return f"{left_str}.{right_str}"
# ----------------------------------------------------------------


def FIND_COIN(Coin):
    full_coinlist = DATA.GET_FULLCOIN()
    for full_coin in full_coinlist[DEF.Wallet_Headers[0]]:
        if full_coin != Coin: continue
        if Coin != "USDT": return True
        break
    MSG.SEND(f"{Coin} coin not available.")
    return False


def USDT_BALANCE(Coin, Balance):
    if Coin[:2] == "LD": coin = Coin[2:]
    else: coin = Coin
    if coin != "USDT":
        price = READ.CANDLE(Coin=coin, Period="1m", Limit=1, Head_ID=4)[0]
        Balance = DATA.FIND_USDT_QUANTITY(Coin_Quantity=Balance, Coin_Price=price)
    if Balance > DEF.MIN_USDT_Balance: return float(round(Balance, 3))
    return 0


def TOTAL_WALLET(Transaction_ID):
    wallet = READ.WALLET()
    total_usdt = 0
    if Transaction_ID == 0:
        for i in range(len(wallet[DEF.Wallet_Headers[0]])): total_usdt += wallet[DEF.Wallet_Headers[2]][i]
    elif Transaction_ID == 1:
        for i in range(len(wallet[DEF.Wallet_Headers[0]])):
            if wallet[DEF.Wallet_Headers[0]][i][:2] != "LD": total_usdt += wallet[DEF.Wallet_Headers[2]][i]
    else:
        for i in range(len(wallet[DEF.Wallet_Headers[0]])):
            if wallet[DEF.Wallet_Headers[0]][i][:2] == "LD": total_usdt += wallet[DEF.Wallet_Headers[2]][i]
    return round(total_usdt, 2)


def COIN_CHANGE(Coin, Days):
    today = LIB.DATE.datetime.now()
    past_day = today - LIB.DATE.timedelta(days=Days)
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    past_day = past_day.strftime("%Y-%m-%d %H:%M:%S")
    try:
        past_price = READ.CANDLE(Coin=Coin, Period="1m", Limit=1, Datetime=past_day, Head_ID=4)
        current_price = READ.CANDLE(Coin=Coin, Period="1m", Limit=1, Datetime=today, Head_ID=4)
        return round(((current_price[0] - past_price[0]) / past_price[0]) * 100, 2)
    except Exception: return 0


def MINLIST():
    try:
        df = READ.COINLIST_CHANGES()
        headers = DEF.Coinlist_Changes_Headers
        min_avglist = LIB.HEAP.nsmallest(int(len(df[headers[6]]) / 2), df[headers[6]])
        min_coinlist = df.loc[df[headers[6]].isin(min_avglist), [headers[0], headers[6]]]
        minlist = min_coinlist.sort_values(headers[6])
        return minlist[headers[0]]
    except Exception as e: MSG.SEND_ERROR(f"FIND_MINLIST: {e}")


def MAXLIST():
    try:
        df = READ.COINLIST_CHANGES()
        headers = DEF.Coinlist_Changes_Headers
        max_avglist = LIB.HEAP.nlargest(int(len(df[headers[6]]) / 2), df[headers[6]])
        max_coinlist = df.loc[df[headers[6]].isin(max_avglist), [headers[0], headers[6]]]
        maxlist = max_coinlist.sort_values(headers[6])
        return maxlist[headers[0]]
    except Exception as e: MSG.SEND_ERROR(f"FIND_MAXLIST: {e}")
# ----------------------------------------------------------------


def COIN_INFO(Coin):
    while True:
        if T.Transaction[T.Coin]: LIB.TIME.sleep(100)
        else: break
    T.Transaction[T.Coin] = True
    if FIND_COIN(Coin):
        prices = READ.CANDLE(Coin=Coin, Period=DEF.Candle_Periods[0], Limit=205, Head_ID=4)
        if len(prices) < 205: MSG.SEND(f"I cannot calculate\nBecause {Coin} is still very new")
        else:
            full_signals = INDICATOR.FULL_SIGNALS(prices)
            signals = ["None"] * 5
            for i in range(len(full_signals)):
                if full_signals[i] == 1: signals[i] = "BUY"
                elif full_signals[i] == -1: signals[i] = "SELL"
            MSG.SEND(f"Coin: {Coin}\nPrice: {float(prices[len(prices)-1])}\nEMA: {signals[0]}\nSMA: {signals[1]}\n"
                     f"Golden Cross: {signals[2]}\nRSI: {signals[3]}\nStochRSI: {signals[4]}\n")
    T.Transaction[T.Coin] = False


def WALLET_CHANGES_INFO():
    wallet = [0] * 3
    for i in range(len(wallet)): wallet[i] = TOTAL_WALLET(i)
    message = f"Total Wallet: {wallet[0]}\nSpot Total Wallet: {wallet[1]}\nEarn Total Wallet: {wallet[2]}\n\n"
    percents = [0] * 6
    headers = [DEF.Wallet_Changes_Headers[1], DEF.Wallet_Changes_Headers[2], DEF.Wallet_Changes_Headers[3],
               DEF.Wallet_Changes_Headers[4], DEF.Wallet_Changes_Headers[5], DEF.Wallet_Changes_Headers[6]]
    change_info = READ.WALLET_CHANGES()
    try:
        for i in range(len(headers)):
            percents[i] = change_info[headers[i]].values[0]
            message += f"{headers[i]}: {percents[i]}\n"
        MSG.SEND(message)
    except Exception as e: MSG.SEND_ERROR(f"WALLET_INFO: {e}")
# ----------------------------------------------------------------
