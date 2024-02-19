# ----------------------------------------------------------------
# Added Links
from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
from src.engine import dataops as DATA
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
# ----------------------------------------------------------------


# Basic Test Algorithms
def DCA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, CANDLE_PERIOD)
    sma25 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[0])
    for i in range(len(openTime)):
        if LIB.PD.isna(sma25[i]) is False:
            signal = INDICATOR.DCA_SIGNAL(closePrice[i - 2], closePrice[i - 1], sma25[i - 2], sma25[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE("DCA", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def EMA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, CANDLE_PERIOD)
    ema25 = INDICATOR.EMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[0])
    for i in range(len(openTime)):
        if LIB.PD.isna(ema25[i]) is False:
            signal = INDICATOR.DCA_SIGNAL(closePrice[i - 2], closePrice[i - 1], ema25[i - 2], ema25[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE("EMA", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def GOLDENCROSS_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, CANDLE_PERIOD)
    sma50 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[1])
    sma200 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[2])
    for i in range(len(openTime)):
        if LIB.PD.isna(sma50[i]) is False:
            signal = INDICATOR.GOLDENCROSS_SIGNAL(sma50[i - 2], sma50[i - 1], sma200[i - 2], sma200[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE("Golden Cross", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def RSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, CANDLE_PERIOD)
    rsi = INDICATOR.RSI(coinSymbol, CANDLE_PERIOD)
    for i in range(len(openTime)):
        if LIB.PD.isna(rsi[i]) is False:
            signal = INDICATOR.RSI_SIGNAL(rsi[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"RSI: {rsi[i - 1]} - {totalCoin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"RSI: {rsi[i - 1]} - {totalCoin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE("RSI", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def STOCHRSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, CANDLE_PERIOD)
    stochRSI = INDICATOR.STOCHRSI(coinSymbol, CANDLE_PERIOD)
    stochRSI_K = stochRSI["stochRSI_K"]
    for i in range(len(openTime)):
        if LIB.PD.isna(stochRSI_K[i]) is False:
            signal = INDICATOR.RSI_SIGNAL(stochRSI_K[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"STOCHRSI: {stochRSI_K[i - 1]} - {totalCoin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"STOCHRSI: {stochRSI_K[i - 1]} - {totalCoin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE("StochRSI", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def MIX_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, CANDLE_PERIOD)
    sma25 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[0])
    ema25 = INDICATOR.EMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[0])
    sma50 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[1])
    sma200 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, DEF.MA_LENGTHS[2])
    rsi = INDICATOR.RSI(coinSymbol, CANDLE_PERIOD)
    stochRSI = INDICATOR.STOCHRSI(coinSymbol, CANDLE_PERIOD)
    stochRSI_K = stochRSI["stochRSI_K"]
    for i in range(len(openTime)):
        if not any(LIB.PD.isna([stochRSI_K[i], rsi[i], sma50[i], sma25[i]])):
            signal = INDICATOR.MIX_SIGNAL(closePrice[i - 2], closePrice[i - 1], sma25[i - 2], sma25[i - 1],
                                          sma50[i - 2], sma50[i - 1], sma200[i - 2], sma200[i - 1], ema25[i - 2],
                                          ema25[i - 1], rsi[i - 1], stochRSI_K[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE("MIX", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def FULL_PERIOD_MIX_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = DATA.READ_CANDLE(coinSymbol, "15m", None, None, 0)
    closePrice = DATA.READ_CANDLE(coinSymbol, "15m", None, None, 4)
    DATA.DELETE_CANDLE(coinSymbol, "15m")
    CALCULATE.SEND_MESSAGE("Full Period Mix Algorithm Calculating (AVG: 9 Minutes)...")
    for i in range(len(openTime)):
        print(f"{i+1}. Candle Reading")
        signal = INDICATOR.FULL_PERIOD_MIX_SIGNAL(coinSymbol, openTime[i])
        if signal == 1 and WALLET != 0:
            print("####################################################")
            totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
            WALLET = 0
            buyNum += 1
            print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
        if signal == -1 and totalCoin != 0:
            print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
            WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
            totalCoin = 0
            sellNum += 1
            print("####################################################")
    CALCULATE.TEST_MESSAGE("MIX and PERIOD", LEFT_SMYBOL, RIGHT_SYMBOL, "15m", WALLET,
                           totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])
# ----------------------------------------------------------------
