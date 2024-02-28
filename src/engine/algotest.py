# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Basic Test Algorithms
def DCA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 4)
    sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], coinSymbol, None, closePrice)
    for i in range(len(openTime)):
        if LIB.PD.isna(sma25[i]) is False:
            signal = SIGNAL.DCA(closePrice[i-2], closePrice[i-1], sma25[i-2], sma25[i-1])
            if signal == 1 and TEST_WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
                TEST_WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST("DCA", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice)-1])


def EMA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 4)
    ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], coinSymbol, None, closePrice)
    for i in range(len(openTime)):
        if LIB.PD.isna(ema25[i]) is False:
            signal = SIGNAL.DCA(closePrice[i-2], closePrice[i-1], ema25[i-2], ema25[i-1])
            if signal == 1 and TEST_WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
                TEST_WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST("EMA", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice)-1])


def GOLDENCROSS_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 4)
    sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], coinSymbol, None, closePrice)
    sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], coinSymbol, None, closePrice)
    for i in range(len(openTime)):
        if LIB.PD.isna(sma50[i]) is False:
            signal = SIGNAL.GOLDENCROSS(sma50[i-2], sma50[i-1], sma200[i-2], sma200[i-1])
            if signal == 1 and TEST_WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
                TEST_WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST("Golden Cross", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice) - 1])


def RSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 4)
    rsi = INDICATOR.RSI(coinSymbol, None, closePrice)
    for i in range(len(openTime)):
        if LIB.PD.isna(rsi[i]) is False:
            signal = SIGNAL.RSI(rsi[i-1])
            if signal == 1 and TEST_WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
                TEST_WALLET = 0
                buyNum += 1
                print(f"RSI: {rsi[i - 1]} - {totalCoin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"RSI: {rsi[i - 1]} - {totalCoin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST("RSI", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice)-1])


def STOCHRSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 4)
    stochRSI = INDICATOR.STOCHRSI(coinSymbol, None, closePrice)
    stochRSI_K = stochRSI["stochRSI_K"]
    for i in range(len(openTime)):
        if LIB.PD.isna(stochRSI_K[i]) is False:
            signal = SIGNAL.RSI(stochRSI_K[i-1])
            if signal == 1 and TEST_WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
                TEST_WALLET = 0
                buyNum += 1
                print(f"STOCHRSI: {stochRSI_K[i-1]} - {totalCoin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"STOCHRSI: {stochRSI_K[i-1]} - {totalCoin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST("StochRSI", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice)-1])


def GOLDENFIVE_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, CANDLE_PERIOD, None, None, 4)
    sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], coinSymbol, None, closePrice)
    ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], coinSymbol, None, closePrice)
    sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], coinSymbol, None, closePrice)
    sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], coinSymbol, None, closePrice)
    rsi = INDICATOR.RSI(coinSymbol, None, closePrice)
    stochRSI = INDICATOR.STOCHRSI(coinSymbol, None, closePrice)
    stochRSI_K = stochRSI["stochRSI_K"]
    for i in range(len(openTime)):
        if not any(LIB.PD.isna([stochRSI_K[i], rsi[i], sma50[i], sma25[i]])):
            goldenNums = INDICATOR.GOLDENFIVE(closePrice[i-2], closePrice[i-1], sma25[i-2], sma25[i-1],
                                              sma50[i-2], sma50[i-1], sma200[i-2], sma200[i-1], ema25[i-2],
                                              ema25[i-1], rsi[i-1], stochRSI_K[i-1])
            signal = SIGNAL.GOLDENFIVE(goldenNums)
            if signal == 1 and TEST_WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
                TEST_WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    MESSAGE.SEND_TEST("Golden Five", LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice)-1])


def FIVEPERIOD_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, TEST_WALLET):
    totalCoin = buyNum = sellNum = 0
    totalInvesment = TEST_WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = CANDLE.READ(coinSymbol, "15m", None, None, 0)
    closePrice = CANDLE.READ(coinSymbol, "15m", None, None, 4)
    MESSAGE.SEND("Full Period Mix Algorithm Calculating (AVG: 9 Minutes)...")
    for i in range(len(openTime)):
        print(f"{i+1}. Candle Reading")
        signal = SIGNAL.FIVEPERIOD(coinSymbol, openTime[i])
        if signal == 1 and TEST_WALLET != 0:
            print("####################################################")
            totalCoin = CALCULATE.TEST_BUY(TEST_WALLET, closePrice[i])
            TEST_WALLET = 0
            buyNum += 1
            print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
        if signal == -1 and totalCoin != 0:
            print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
            TEST_WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
            totalCoin = 0
            sellNum += 1
            print("####################################################")
    MESSAGE.SEND_TEST("Five Period", LEFT_SMYBOL, RIGHT_SYMBOL, "15m", TEST_WALLET,
                      totalCoin, totalInvesment, buyNum, sellNum, closePrice[len(closePrice)-1])
# ----------------------------------------------------------------
