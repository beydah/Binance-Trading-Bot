# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import indicator as INDICATOR
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import bot as BOT
from src.engine.message import message as MESSAGE
from src.engine.message import transactions as TRANSACTIONS
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# THREAD
from src.engine.thread import timer as TIMER
from src.engine.thread import debugger as DEBUGGER
from src.engine.thread import processor as PROCESSOR
# ----------------------------------------------------------------


# Order Calculations
def TEST_BUY(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY / WEALTH_PRICE
    commission = coinQuantity * DEF.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    coinQuantity = round(coinQuantity, 6)
    return coinQuantity


def TEST_SELL(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY * WEALTH_PRICE
    commission = coinQuantity * DEF.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    coinQuantity = round(coinQuantity, 6)
    return coinQuantity
# ----------------------------------------------------------------


def USDT_BALANCE(COIN, BALANCE):
    if COIN[:2] == "LD": coin = COIN[2:]
    else: coin = COIN
    if coin != "USDT":
        closePrice = READ.CANDLE(coin, "1m", None, 1, 4)
        USDTBalance = closePrice[0] * BALANCE
    else: USDTBalance = BALANCE
    if USDTBalance < 0.01: return 0
    return round(USDTBalance, 2)


def TOTAL_WALLET(TRANSACTION_ID):
    df = READ.WALLET()
    coin = df["Coin"]
    USDTBalance = df["USDT_Balance"]
    totalUSDT = 0
    if TRANSACTION_ID == 0:
        for i in range(len(coin)): totalUSDT += USDTBalance[i]
    elif TRANSACTION_ID == 1:
        for i in range(len(coin)):
            if coin[i][:2] != "LD": totalUSDT += USDTBalance[i]
    else:
        for i in range(len(coin)):
            if coin[i][:2] == "LD": totalUSDT += USDTBalance[i]
    return round(totalUSDT, 2)


def COIN_CHANGE(COIN, DAYS):
    past = LIB.DATE.timedelta(days=DAYS)
    today = LIB.DATE.datetime.now()
    pastDay = today - past
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    pastDay = pastDay.strftime("%Y-%m-%d %H:%M:%S")
    try:
        pastPrices = READ.CANDLE(COIN, "1m", pastDay, 1, 4)
        currentPrices = READ.CANDLE(COIN, "1m", today, 1, 4)
        pastPrice = pastPrices[len(pastPrices) - 1]
        currentPrice = currentPrices[len(currentPrices) - 1]
        priceDifference = currentPrice - pastPrice
        percentChange = round((priceDifference / pastPrice) * 100, 4)
    except Exception: percentChange = 0
    return percentChange


def SEARCH_COIN(COIN):
    fullCoinList = DATA.GET_FULLCOIN()
    for fullCoin in fullCoinList["Coin"]:
        if fullCoin == COIN:
            if COIN == "USDT": break
            return True
    MESSAGE.SEND(f"{COIN} coin not available.")
    return False


def COIN_INFO(COIN):
    if DATA.FIND_COIN(COIN):
        closePrice = READ.CANDLE(COIN, "30m", CANDLE_LIMIT=205, HEAD_ID=4)
        sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], closePrice)
        ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], closePrice)
        sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], closePrice)
        sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], closePrice)
        rsi = INDICATOR.RSI(closePrice)
        stochRSI = INDICATOR.STOCHRSI(closePrice)
        old = len(closePrice) - 3
        last = len(closePrice) - 2
        signals = ["None", "None", "None", "None", "None"]
        indicatorSignals = [0, 0, 0, 0, 0]
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
    wallet = [0, 0, 0]
    for i in range(3): wallet[i] = DATA.GET_TOTAL_WALLET(i)
    changeInfo = READ.WALLET_CHANGES()
    D1_Percent = changeInfo["1D_Percent"].values[0]
    D3_Percent = changeInfo["3D_Percent"].values[0]
    D7_Percent = changeInfo["7D_Percent"].values[0]
    D15_Percent = changeInfo["15D_Percent"].values[0]
    D30_Percent = changeInfo["30D_Percent"].values[0]
    AVG_Percent = changeInfo["AVG_Percent"].values[0]
    MESSAGE.SEND(f"Total Wallet: {wallet[0]}\nSpot Total Wallet: {wallet[1]}\nEarn Total Wallet: {wallet[2]}\n\n"
                 f"Changes Info:\n1 Day Percent: {D1_Percent}\n3 Day Percent: {D3_Percent}\n"
                 f"7 Day Percent: {D7_Percent}\n15 Day Percent: {D15_Percent}\n"
                 f"30 Day Percent: {D30_Percent}\nAVG Percent: {AVG_Percent}\n")
# ----------------------------------------------------------------
