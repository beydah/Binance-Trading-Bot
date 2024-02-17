# ----------------------------------------------------------------
# Added Links
from src.business import business as B
from src.business import calculator as CALCULATE
from src.business import indicator as INDICATOR
from src.settings import settings as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Basic Test Algorithms
def DCA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "DCA"
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    sma25Length = LIB.MA_LENGTHS[0]
    sma25 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, sma25Length)
    for i in range(len(closePrice)):
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
    CALCULATE.TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                           totalCoin, buyNum, sellNum, closePrice[len(closePrice) - 1], totalInvesment)


def EMA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "EMA"
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    ema25Length = LIB.MA_LENGTHS[0]
    ema25 = INDICATOR.EMA(coinSymbol, CANDLE_PERIOD, ema25Length)
    for i in range(len(closePrice)):
        if LIB.PD.isna(ema25[i]) is False:
            signal = INDICATOR.EMA_SIGNAL(closePrice[i - 2], closePrice[i - 1], ema25[i - 2], ema25[i - 1])
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
    CALCULATE.TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                           totalCoin, buyNum, sellNum, closePrice[len(closePrice) - 1], totalInvesment)


def GOLDENCROSS_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "Golden Cross"
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    sma50Length = LIB.MA_LENGTHS[1]
    sma50 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, sma50Length)
    sma200Length = LIB.MA_LENGTHS[2]
    sma200 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, sma200Length)
    for i in range(len(closePrice)):
        if LIB.PD.isna(sma50[i]) is False:
            signal = INDICATOR.GOLDENCROSS_SIGNAL(sma50[i - 2], sma200[i - 2], sma50[i - 1], sma200[i - 1])
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
    CALCULATE.TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                           totalCoin, buyNum, sellNum, closePrice[len(closePrice) - 1], totalInvesment)


def RSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "RSI"
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    RSI = INDICATOR.RSI(coinSymbol, CANDLE_PERIOD)
    for i in range(len(closePrice)):
        if LIB.PD.isna(RSI[i]) is False:
            signal = INDICATOR.RSI_SIGNAL(RSI[i - 1])
            if signal == 1 and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"RSI: {RSI[i - 1]} - {totalCoin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if signal == -1 and totalCoin != 0:
                print(f"RSI: {RSI[i - 1]} - {totalCoin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, closePrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                           totalCoin, buyNum, sellNum, closePrice[len(closePrice) - 1], totalInvesment)


def STOCHRSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "StochRSI"
    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    stochRSI = INDICATOR.STOCHRSI(coinSymbol, CANDLE_PERIOD)
    stochRSI_K = stochRSI["stochRSI_K"]
    for i in range(len(closePrice)):
        if LIB.PD.isna(stochRSI_K[i]) is False:
            signal = INDICATOR.STOCHRSI_SIGNAL(stochRSI_K[i - 1])
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
    CALCULATE.TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                           totalCoin, buyNum, sellNum, closePrice[len(closePrice) - 1], totalInvesment)


def MIX_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "MIX"

    totalCoin = buyNum = sellNum = 0
    totalInvesment = WALLET
    coinSymbol = LEFT_SMYBOL + RIGHT_SYMBOL
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, None, 4)
    sma25Length = LIB.MA_LENGTHS[0]
    sma25 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, sma25Length)
    ema25Length = LIB.MA_LENGTHS[0]
    ema25 = INDICATOR.EMA(coinSymbol, CANDLE_PERIOD, ema25Length)
    sma50Length = LIB.MA_LENGTHS[1]
    sma50 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, sma50Length)
    sma200Length = LIB.MA_LENGTHS[2]
    sma200 = INDICATOR.SMA(coinSymbol, CANDLE_PERIOD, sma200Length)
    RSI = INDICATOR.RSI(coinSymbol, CANDLE_PERIOD)
    stochRSI = INDICATOR.STOCHRSI(coinSymbol, CANDLE_PERIOD)
    stochRSI_K = stochRSI["stochRSI_K"]
    for i in range(len(closePrice)):
        if not any(LIB.PD.isna([stochRSI_K[i], RSI[i], sma50[i], sma25[i]])):
            signal = INDICATOR.MIX_SIGNAL(closePrice[i-2], closePrice[i-1], sma25[i-2], sma25[i-1],
                                          sma50[i-2], sma50[i-1], sma200[i-2], sma200[i-1],
                                          ema25[i-2], ema25[i-1], stochRSI_K[i-1], RSI[i-1])
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
    CALCULATE.TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                           totalCoin, buyNum, sellNum, closePrice[len(closePrice) - 1], totalInvesment)
# ----------------------------------------------------------------
