# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.math import indicator as INDICATOR
# MESSAGE
from src.engine.message import message as MSG
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


# Order Calculations
def MARKET_BUY(Coin, Quantity):
    virtual_quantity = VIRTUAL_QUANTITY("Market Buy", Coin, LIB.DECIMAL(Quantity))
    if virtual_quantity is None: return False
    client = DATA.GET_BINANCE()
    while True:
        try:
            client.order_market(symbol=Coin+"USDT", side="BUY", quantity=virtual_quantity)
            break
        except Exception as e: MSG.SEND_ERROR(f"MARKET_BUY: {e}")
    MSG.SEND(f"{virtual_quantity} {Coin} - Buy")
    return True


def MARKET_SELL(Coin, Quantity):
    virtual_quantity = VIRTUAL_QUANTITY("Market Sell", Coin, LIB.DECIMAL(Quantity))
    if virtual_quantity is None: return False
    client = DATA.GET_BINANCE()
    while True:
        try:
            client.order_market(symbol=Coin+"USDT", side="SELL", quantity=virtual_quantity)
            break
        except Exception as e: MSG.SEND_ERROR(f"MARKET_SELL: {e}")
    MSG.SEND(f"{virtual_quantity} {Coin} - Sell")
    return True


def CREATE_STOP_LOSS(Coin):
    balance = READ.WALLET(Coin, 1)
    virtual_quantity = VIRTUAL_QUANTITY("Create Stop Loss", Coin, LIB.DECIMAL(balance.item()))
    if virtual_quantity is None: return False
    client = DATA.GET_BINANCE()
    while True:
        try:
            price = READ.CANDLE(Coin=Coin, Period="1m", Limit=1, Head_ID=4)
            price_step = len(str(price[0]).split(".")[-1])
            stop_price = round(float(price[0]) * DEF.Stop_Loss_Rate, price_step)
            client.create_order(symbol=Coin+"USDT", type="STOP_LOSS_LIMIT", side="SELL",
                                price=stop_price, stopPrice=stop_price, quantity=virtual_quantity, timeInForce="GTC")
            break
        except Exception as e: MSG.SEND_ERROR(f"CREATE_STOP_LOSS: {e}")
    MSG.SEND(f"{Coin} Buy Price: {float(price[0])}\n{Coin} Stop Loss Price - {float(stop_price)}\n")
    return True


def DELETE_STOP_LOSS(Coin):
    client = DATA.GET_BINANCE()
    while True:
        try:
            open_orders = client.get_open_orders(symbol=Coin+"USDT")
            if open_orders is None: return False
            stop_loss_order = None
            for order in open_orders:
                if order['type'] == 'STOP_LOSS_LIMIT' and order['side'] == 'SELL':
                    stop_loss_order = order
                    break
            if stop_loss_order is None: return False
            client.cancel_order(symbol=Coin+"USDT", orderId=stop_loss_order['orderId'])
            break
        except Exception as e: MSG.SEND_ERROR(f"DELETE_STOP_LOSS: {e}")
    return True


def TEST_BUY(USDT, Coin_Price): return DEF.Binance_Comission_Rate * DATA.FIND_COIN_QUANTITY(USDT, Coin_Price)


def TEST_SELL(Coin, Coin_Price): return DEF.Binance_Comission_Rate * DATA.FIND_USDT_QUANTITY(Coin, Coin_Price)
# ----------------------------------------------------------------


def VIRTUAL_QUANTITY(Transaction, Coin, Quantity):
    qty = [DATA.GET_SYMBOLINFO(Coin, Info="minQty"), DATA.GET_SYMBOLINFO(Coin, Info="maxQty")]
    if LIB.DECIMAL(qty[0]) > Quantity:
        MSG.SEND(f"I can't {Transaction} {Coin}\nBeacuse Min Quantity: {float(qty[0])}\n"
                 f"My Request Quantity: {float(Quantity)}\n")
        return None
    if LIB.DECIMAL(qty[1]) < Quantity: Quantity = LIB.DECIMAL(qty[1])
    min_step = 0
    for char in qty[0]:
        if char == "0": min_step += 1
        elif char == "1": break
    if Quantity == int(Quantity): str_quantity = f"{int(Quantity)}."+("0" * 8)
    else: str_quantity = str(LIB.DECIMAL(Quantity))
    left_str, right_str = str_quantity.split(".")
    right_str = right_str[:min_step]
    if right_str == "": return left_str
    return f"{left_str}.{right_str}"
# ----------------------------------------------------------------


def USDT_BALANCE(Coin, Balance):
    if Coin[:2] == "LD": coin = Coin[2:]
    else: coin = Coin
    if coin != "USDT":
        price = READ.CANDLE(Coin=coin, Period="1m", Limit=1, Head_ID=4)
        Balance = DATA.FIND_USDT_QUANTITY(Balance, price[0])
    if Balance > DEF.MIN_USDT_Balance: return float(round(Balance, 3))
    return 0


def TOTAL_WALLET(Transaction_ID):
    wallet = READ.WALLET()
    total_usdt = 0
    if Transaction_ID == 0:
        for i in range(len(wallet["Coin"])): total_usdt += wallet["USDT Balance"][i]
    elif Transaction_ID == 1:
        for i in range(len(wallet["Coin"])):
            if wallet["Coin"][i][:2] != "LD": total_usdt += wallet["USDT Balance"][i]
    else:
        for i in range(len(wallet["Coin"])):
            if wallet["Coin"][i][:2] == "LD": total_usdt += wallet["USDT Balance"][i]
    return round(total_usdt, 2)


def COIN_CHANGE(Coin, Days):
    today = LIB.DATE.datetime.now()
    past_day = today - LIB.DATE.timedelta(days=Days)
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    past_day = past_day.strftime("%Y-%m-%d %H:%M:%S")
    try:
        past_price = READ.CANDLE(Coin=Coin, Period="1m", Datetime=past_day, Limit=1, Head_ID=4)
        current_price = READ.CANDLE(Coin=Coin, Period="1m", Datetime=today, Limit=1, Head_ID=4)
        return round(((current_price[0] - past_price[0]) / past_price[0]) * 100, 2)
    except Exception: return 0


def FIND_COIN(Coin):
    full_coinlist = DATA.GET_FULLCOIN()
    for full_coin in full_coinlist["Coin"]:
        if full_coin != Coin: continue
        if Coin != "USDT": return True
        break
    MSG.SEND(f"{Coin} coin not available.")
    return False
# ----------------------------------------------------------------


def COIN_INFO(Coin):
    if FIND_COIN(Coin):
        price = READ.CANDLE(Coin=Coin, Period=DEF.Candle_Periods[0], Limit=205, Head_ID=4)
        if len(price) < 205:
            MSG.SEND(f"I cannot calculate\nBecause {Coin} is still very new")
            return None
        sma25 = INDICATOR.SMA(DEF.MA_Lengths[0], price)
        ema25 = INDICATOR.EMA(DEF.MA_Lengths[0], price)
        sma50 = INDICATOR.SMA(DEF.MA_Lengths[1], price)
        sma200 = INDICATOR.SMA(DEF.MA_Lengths[2], price)
        rsi = INDICATOR.RSI(price)
        stochRSI = INDICATOR.STOCHRSI(price)
        indicator_signal = [0] * 5
        signals = ["None"] * 5
        last = len(price) - 2
        if not any(LIB.PD.isna([stochRSI[last-1], rsi[last-1], sma200[last-1], sma50[last-1], sma25[last-1]])):
            indicator_signal[0] = INDICATOR.DCA_SIGNAL(price[last-1], price[last], sma25[last-1], sma25[last])
            indicator_signal[1] = INDICATOR.DCA_SIGNAL(price[last-1], price[last], ema25[last-1], ema25[last])
            indicator_signal[2] = INDICATOR.GOLDENCROSS_SIGNAL(sma50[last-1], sma50[last], sma200[last-1], sma200[last])
            indicator_signal[3] = INDICATOR.RSI_SIGNAL(rsi[last])
            indicator_signal[4] = INDICATOR.RSI_SIGNAL(stochRSI[last])
            for i in range(len(indicator_signal)):
                if indicator_signal[i] == 1: signals[i] = "BUY"
                elif indicator_signal[i] == -1: signals[i] = "SELL"
        MSG.SEND(f"Coin: {Coin}\nPrice: {float(price[len(price) - 1])}\n"
                 f"SMA: {signals[0]}\nEMA: {signals[1]}\n"
                 f"Golden Cross: {signals[2]}\nRSI: {signals[3]}\n"
                 f"StochRSI: {signals[4]}\n")


def WALLET_INFO():
    wallet = [0] * 3
    for i in range(len(wallet)): wallet[i] = TOTAL_WALLET(i)
    message = f"Total Wallet: {wallet[0]}\nSpot Total Wallet: {wallet[1]}\nEarn Total Wallet: {wallet[2]}\n\n"
    percents = [0] * 6
    percents_headers = [
        "1 Day Percent", "3 Day Percent", "7 Day Percent", "15 Day Percent", "30 Day Percent", "AVG Percent"]
    change_info = READ.WALLET_CHANGES()
    try:
        for i in range(len(percents_headers)): percents[i] = change_info[percents_headers[i]].values[0]
        for i in range(len(percents_headers)): message += f"{percents_headers[i]}: {percents[i]}\n"
        MSG.SEND(message)
    except Exception as e: MSG.SEND_ERROR(f"WALLET_INFO: {e}")
# ----------------------------------------------------------------
