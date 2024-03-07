# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import indicator as INDICATOR
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


# Backtest
def TEST(COIN):
    if DATA.FIND_COIN(COIN):
        for period in DEF.CANDLE_PEROIDS: GOLDENFIVE(COIN, period, 1000)


def GOLDENFIVE(COIN, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    openTime = READ.CANDLE(COIN, CANDLE_PERIOD, HEAD_ID=0)
    closePrice = READ.CANDLE(COIN, CANDLE_PERIOD, HEAD_ID=4)
    sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], closePrice)
    ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], closePrice)
    sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], closePrice)
    sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], closePrice)
    rsi = INDICATOR.RSI(closePrice)
    stochRSI = INDICATOR.STOCHRSI(closePrice)
    for i in range(len(openTime)):
        if not any(LIB.PD.isna([stochRSI[i], rsi[i], sma50[i], sma25[i]])):
            goldenNums = INDICATOR.GOLDENFIVE(closePrice[i-2], closePrice[i-1],
                                              sma25[i-2], sma25[i-1], sma50[i-2], sma50[i-1],
                                              sma200[i-2], sma200[i-1], ema25[i-2], ema25[i-1],
                                              rsi[i-1], stochRSI[i-1])
            signal = INDICATOR.GOLDENFIVE_SIGNAL(goldenNums)
            if signal == 1 and WALLET > 0:
                print("####################################################")
                buyNum += 1
                WALLET = 0
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                print(f"{totalCoin} - {COIN} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin > 0:
                print(f"{totalCoin} - {COIN} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST(COIN, CANDLE_PERIOD, WALLET, totalCoin, totalInvesment,
                      buyNum, sellNum, closePrice[len(closePrice)-1])
# ----------------------------------------------------------------
