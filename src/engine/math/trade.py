# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import indicator as INDICATOR
# MESSAGE
from src.engine.message import message as MESSAGE
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


# Backtest
def TEST(PROMPT):
    PROMPT = PROMPT.replace(" ", "")
    coin = entryWallet = monthlyAddition = None
    if "," in PROMPT:
        if PROMPT.count(",") == 1: coin, entryWallet = PROMPT.split(",")
        elif PROMPT.count(",") == 2: coin, entryWallet, monthlyAddition = PROMPT.split(",")
    else: coin = PROMPT
    try: entryWallet = int(entryWallet)
    except: entryWallet = 1000
    try: monthlyAddition = int(monthlyAddition)
    except: monthlyAddition = 100
    if CALCULATE.FIND_COIN(coin):
        for period in DEF.CANDLE_PERIODS: GOLDENFIVE(coin, period, entryWallet, monthlyAddition)


def GOLDENFIVE(COIN, CANDLE_PERIOD, WALLET, MONTHLY_ADDITION):
    totalInvesment = entryWallet = WALLET
    totalCoin = buyNum = sellNum = 0
    openTime = READ.CANDLE(COIN=COIN, PERIOD=CANDLE_PERIOD, HEAD_ID=0)
    closePrice = READ.CANDLE(COIN=COIN, PERIOD=CANDLE_PERIOD, HEAD_ID=4)
    sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], closePrice)
    ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], closePrice)
    sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], closePrice)
    sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], closePrice)
    rsi = INDICATOR.RSI(closePrice)
    stochRSI = INDICATOR.STOCHRSI(closePrice)
    openTimeFormat = LIB.DATE.datetime.strptime(openTime[0], "%Y-%m-%d %H:%M:%S")
    oldMonth = openTimeFormat.strftime("%m")
    firstTransactionDate = openTime[len(openTime)-1]
    lastTransactionDate = openTime[0]
    for i in range(len(openTime)):
        openTimeFormat = LIB.DATE.datetime.strptime(openTime[i], "%Y-%m-%d %H:%M:%S")
        if openTimeFormat.strftime("%m") != oldMonth:
            oldMonth = openTimeFormat.strftime("%m")
            WALLET += MONTHLY_ADDITION
            totalInvesment += MONTHLY_ADDITION
        if not any(LIB.PD.isna([stochRSI[i], rsi[i], sma50[i], sma25[i]])):
            signal = INDICATOR.GOLDENFIVE_SIGNAL(
                INDICATOR.GOLDENFIVE(closePrice[i-2], closePrice[i-1], sma25[i-2], sma25[i-1],
                                     sma50[i-2], sma50[i-1], sma200[i-2], sma200[i-1],
                                     ema25[i-2], ema25[i-1], rsi[i-1], stochRSI[i-1]))
            if signal == 1 or signal == -1:
                if openTime[i] < firstTransactionDate: firstTransactionDate = openTime[i]
                if openTime[i] > lastTransactionDate: lastTransactionDate = openTime[i]
                if signal == 1 and WALLET != 0:
                    print("####################################################")
                    totalCoin += CALCULATE.TEST_BUY(WALLET, closePrice[i])
                    WALLET = 0
                    buyNum += 1
                    print(f"{totalCoin} - {COIN} - BUY - {openTime[i]}")
                elif signal == -1 and totalCoin != 0:
                    print(f"{totalCoin} - {COIN} - SELL - {openTime[i]}")
                    WALLET += CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                    totalCoin = 0
                    sellNum += 1
                    print("####################################################")
    MESSAGE.SEND_TEST(COIN, CANDLE_PERIOD, firstTransactionDate, lastTransactionDate, buyNum, sellNum,
                      entryWallet, MONTHLY_ADDITION, totalInvesment, totalCoin, closePrice[len(closePrice) - 1], WALLET)


def BEYZA_STOP():
    if DEF.TRADE_STOP is False: return None
    wallet = READ.WALLET()
    if not wallet.empty:
        for i in range(len(wallet["Coin"])):
            if (wallet["Coin"][i][:2] == "LD" or wallet["Coin"][i] == "USDT"
                or wallet["USDT_Balance"][i] <= DEF.MIN_USDT_BALANCE): continue
            CALCULATE.DELETE_STOP_LOSS(wallet["Coin"][i])
            CALCULATE.MARKET_SELL(wallet["Coin"][i], wallet["Balance"][i])
    MESSAGE.SEND("I'm stopped.")


def BEYZA_START():
    MESSAGE.SEND("I'm starting...")
    while True:
        if DEF.TRADE_STOP is True: return None
        wallet = READ.WALLET()
        if not wallet.empty:
            for i in range(len(wallet["Coin"])):
                if DEF.TRADE_STOP is True: return None
                if (wallet["Coin"][i][:2] == "LD" or wallet["Coin"][i] == "USDT"
                    or wallet["USDT_Balance"][i] <= DEF.MIN_USDT_BALANCE): continue
                closePrice = READ.CANDLE(COIN=wallet["Coin"][i], LIMIT=205, HEAD_ID=4)
                sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], closePrice)
                ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], closePrice)
                sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], closePrice)
                sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], closePrice)
                rsi = INDICATOR.RSI(closePrice)
                stochRSI = INDICATOR.STOCHRSI(closePrice)
                old = len(closePrice)-3
                last = len(closePrice)-2
                if not any(LIB.PD.isna([stochRSI[old], rsi[old], sma200[old], sma50[old], sma25[old]])):
                    signal = INDICATOR.GOLDENFIVE_SIGNAL(
                        INDICATOR.GOLDENFIVE(closePrice[old], closePrice[last], sma25[old], sma25[last],
                                             sma50[old], sma50[last], sma200[old], sma200[last],
                                             ema25[old], ema25[last], rsi[last], stochRSI[last]))
                    signal = -1
                    if signal == -1:
                        CALCULATE.DELETE_STOP_LOSS(wallet["Coin"][i])
                        CALCULATE.MARKET_SELL(wallet["Coin"][i], wallet["Balance"][i])
        favoriteList = READ.FAVORITELIST()
        if not favoriteList.empty:
            for coin in favoriteList["Coin"]:
                if DEF.TRADE_STOP is True: return None
                USDTBalance = READ.WALLET("USDT", 2)
                if USDTBalance.empty or USDTBalance.item() / 2 <= DEF.MIN_USDT_BALANCE: continue
                USDT = USDTBalance.item() / 2
                closePrice = READ.CANDLE(COIN=coin, LIMIT=205, HEAD_ID=4)
                sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], closePrice)
                ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], closePrice)
                sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], closePrice)
                sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], closePrice)
                rsi = INDICATOR.RSI(closePrice)
                stochRSI = INDICATOR.STOCHRSI(closePrice)
                old = len(closePrice) - 3
                last = len(closePrice) - 2
                if not any(LIB.PD.isna([stochRSI[old], rsi[old], sma200[old], sma50[old], sma25[old]])):
                    signal = INDICATOR.GOLDENFIVE_SIGNAL(
                        INDICATOR.GOLDENFIVE(closePrice[old], closePrice[last], sma25[old], sma25[last],
                                             sma50[old], sma50[last], sma200[old], sma200[last],
                                             ema25[old], ema25[last], rsi[last], stochRSI[last]))
                    signal = 1
                    if signal == 1:
                        closePrice = READ.CANDLE(COIN=coin, PERIOD="1m", LIMIT=1, HEAD_ID=4)
                        coinQuantity = DATA.FIND_COIN_QUANTITY(USDT, closePrice[len(closePrice) - 1])
                        trade = CALCULATE.MARKET_BUY(coin, coinQuantity)
                        if not trade: continue
                        CALCULATE.CREATE_STOP_LOSS(coin)
        MESSAGE.SEND("I AM WAIT")
        LIB.TIME.sleep(30)
        MESSAGE.SEND("I AM BEGIN AGAIN")
        # LIB.TIME.sleep(900)
# ----------------------------------------------------------------
