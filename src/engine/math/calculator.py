# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.math import indicator as INDICATOR
# MESSAGE
from src.engine.message import message as MESSAGE
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


# Order Calculations
def MARKET_BUY(COIN, QUANTITY):
    virtualQuantity = VIRTUAL_QUANTITY("Market Buy", COIN, QUANTITY)
    if virtualQuantity is None: return False
    client = DATA.GET_BINANCE()
    client.order_market(symbol=COIN+"USDT", side="BUY", quantity=virtualQuantity)
    MESSAGE.SEND(f"{virtualQuantity} {COIN} - BUY")
    return True


def MARKET_SELL(COIN, QUANTITY):
    virtualQuantity = VIRTUAL_QUANTITY("Market Sell", COIN, QUANTITY)
    if virtualQuantity is None: return False
    client = DATA.GET_BINANCE()
    client.order_market(symbol=COIN+"USDT", side="SELL", quantity=virtualQuantity)
    MESSAGE.SEND(f"{virtualQuantity} {COIN} - SELL")
    return True


def CREATE_STOP_LOSS(COIN):
    balance = READ.WALLET(COIN, 1)
    virtualQuantity = VIRTUAL_QUANTITY("Create Stop Loss", COIN, float(balance.item()))
    if virtualQuantity is None: return False
    client = DATA.GET_BINANCE()
    price = READ.CANDLE(COIN=COIN, PERIOD="1m", LIMIT=1, HEAD_ID=4)
    priceStep = len(str(price[0]).split(".")[-1])
    stopPrice = round(float(price[0]) * DEF.STOP_LOSS_RATE, priceStep)
    client.create_order(symbol=COIN+"USDT", type="STOP_LOSS_LIMIT", side="SELL",
                        price=stopPrice, stopPrice=stopPrice, quantity=virtualQuantity, timeInForce="GTC")
    MESSAGE.SEND(f"{COIN} BUY PRICE: {float(price[0])}\n{COIN} STOP LOSS PRICE - {float(stopPrice)}\n")
    return True


def DELETE_STOP_LOSS(COIN):
    client = DATA.GET_BINANCE()
    openOrders = client.get_open_orders(symbol=COIN + "USDT")
    if openOrders is None: return False
    stopLossOrder = None
    for order in openOrders:
        if order['type'] == 'STOP_LOSS_LIMIT' and order['side'] == 'SELL':
            stopLossOrder = order
            break
    if stopLossOrder is None: return False
    client.cancel_order(symbol=COIN + "USDT", orderId=stopLossOrder['orderId'])
    return True


def TEST_BUY(USDT, COIN_PRICE): return DEF.BINANCE_COMISSION_RATE * DATA.FIND_COIN_QUANTITY(USDT, COIN_PRICE)


def TEST_SELL(COIN, COIN_PRICE): return DEF.BINANCE_COMISSION_RATE * DATA.FIND_USDT_QUANTITY(COIN, COIN_PRICE)
# ----------------------------------------------------------------


def VIRTUAL_QUANTITY(TRANSACTION, COIN, QUANTITY):
    minQty = DATA.GET_SYMBOLINFO("MIN QTY", COIN)
    maxQty = DATA.GET_SYMBOLINFO("MAX QTY", COIN)
    if float(minQty) > QUANTITY:
        MESSAGE.SEND(f"I can't {TRANSACTION} {COIN}.\nBeacuse Min Quantity: {float(minQty)}\n"
                     f"My Request Quantity: {float(QUANTITY)}\n")
        return None
    if float(maxQty) < QUANTITY: QUANTITY = float(maxQty)
    minStep = 0
    for char in minQty:
        if char == "0": minStep += 1
        elif char == "1": break
    strQuantity = str(float(QUANTITY))+("0"*8)
    leftStr, rightStr = strQuantity.split(".")
    rightStr = rightStr[:minStep]
    if rightStr == "": return leftStr
    return leftStr+"."+rightStr
# ----------------------------------------------------------------


def USDT_BALANCE(COIN, BALANCE):
    if COIN[:2] == "LD": coin = COIN[2:]
    else: coin = COIN
    if coin != "USDT":
        closePrice = READ.CANDLE(COIN=coin, PERIOD="1m", LIMIT=1, HEAD_ID=4)
        BALANCE = DATA.FIND_USDT_QUANTITY(BALANCE, closePrice[0])
    if BALANCE > DEF.MIN_USDT_BALANCE: return float(round(BALANCE, 3))
    return 0.000


def COIN_BALANCE(COIN, BALANCE):
    if COIN[:2] == "LD": coin = COIN[2:]
    else: coin = COIN
    if coin != "USDT":
        closePrice = READ.CANDLE(COIN=coin, PERIOD="1m", LIMIT=1, HEAD_ID=4)
        BALANCE = FIND_COIN_QUANTITY(BALANCE, closePrice[0])
        if BALANCE > 0: return float(round(BALANCE, 9))


def TOTAL_WALLET(TRANSACTION_ID):
    wallet = READ.WALLET()
    totalUSDT = 0
    if TRANSACTION_ID == 0:
        for i in range(len(wallet["Coin"])): totalUSDT += wallet["USDT_Balance"][i]
    elif TRANSACTION_ID == 1:
        for i in range(len(wallet["Coin"])):
            if wallet["Coin"][i][:2] != "LD": totalUSDT += wallet["USDT_Balance"][i]
    else:
        for i in range(len(wallet["Coin"])):
            if wallet["Coin"][i][:2] == "LD": totalUSDT += wallet["USDT_Balance"][i]
    return round(totalUSDT, 2)


def COIN_CHANGE(COIN, DAYS):
    past = LIB.DATE.timedelta(days=DAYS)
    today = LIB.DATE.datetime.now()
    pastDay = today - past
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    pastDay = pastDay.strftime("%Y-%m-%d %H:%M:%S")
    try:
        pastPrice = READ.CANDLE(COIN=COIN, PERIOD="1m", DATETIME=pastDay, LIMIT=1, HEAD_ID=4)
        currentPrice = READ.CANDLE(COIN=COIN, PERIOD="1m", DATETIME=today, LIMIT=1, HEAD_ID=4)
        priceDifference = currentPrice[0] - pastPrice[0]
        percentChange = (priceDifference / pastPrice[0]) * 100
    except Exception: percentChange = 0
    return float(round(percentChange, 2))


def FIND_COIN(COIN):
    fullCoinList = DATA.GET_FULLCOIN()
    for fullCoin in fullCoinList["Coin"]:
        if fullCoin != COIN: continue
        if COIN != "USDT": return True
        break
    MESSAGE.SEND(f"{COIN} coin not available.")
    return False


def COIN_INFO(COIN):
    if FIND_COIN(COIN):
        closePrice = READ.CANDLE(COIN=COIN, PERIOD="30m", LIMIT=205, HEAD_ID=4)
        sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], closePrice)
        ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], closePrice)
        sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], closePrice)
        sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], closePrice)
        rsi = INDICATOR.RSI(closePrice)
        stochRSI = INDICATOR.STOCHRSI(closePrice)
        indicatorSignals = [0] * 5
        signals = ["None"] * 5
        old = len(closePrice) - 3
        last = len(closePrice) - 2
        if not any(LIB.PD.isna([stochRSI[old], rsi[old], sma200[old], sma50[old], sma25[old]])):
            indicatorSignals[0] = INDICATOR.DCA_SIGNAL(closePrice[old], closePrice[last], sma25[old], sma25[last])
            indicatorSignals[1] = INDICATOR.DCA_SIGNAL(closePrice[old], closePrice[last], ema25[old], ema25[last])
            indicatorSignals[2] = INDICATOR.GOLDENCROSS_SIGNAL(sma50[old], sma50[last], sma200[old], sma200[last])
            indicatorSignals[3] = INDICATOR.RSI_SIGNAL(rsi[last])
            indicatorSignals[4] = INDICATOR.RSI_SIGNAL(stochRSI[last])
            for i in range(5):
                if indicatorSignals[i] == 1: signals[i] = "BUY"
                elif indicatorSignals[i] == -1: signals[i] = "SELL"
        MESSAGE.SEND(f"Coin: {COIN}\nPrice: {float(closePrice[len(closePrice) - 1])}\n"
                     f"SMA: {signals[0]}\nEMA: {signals[1]}\n"
                     f"Golden Cross: {signals[2]}\nRSI: {signals[3]}\n"
                     f"StochRSI: {signals[4]}\n")


def WALLET_INFO():
    wallet = [0] * 3
    for i in range(len(wallet)): wallet[i] = TOTAL_WALLET(i)
    message = f"Total Wallet: {wallet[0]}\nSpot Total Wallet: {wallet[1]}\nEarn Total Wallet: {wallet[2]}\n\n"
    percents = [0] * 6
    changeInfo = READ.WALLET_CHANGES()
    percentsHeaders = ["1D_Percent", "3D_Percent", "7D_Percent", "15D_Percent", "30D_Percent", "AVG_Percent"]
    try:
        for i in range(len(percentsHeaders)): percents[i] = changeInfo[percentsHeaders[i]].values[0]
        for i in range(len(percentsHeaders)): message += f"{percentsHeaders[i]}: {percents[i]}\n"
        MESSAGE.SEND(message)
    except Exception as e: MESSAGE.SEND_ERROR(f"WALLET_INFO: {e}")
# ----------------------------------------------------------------
