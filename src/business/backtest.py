# Added Pages
from src.settings import settings as S
from src.business import business as B
from src.business import calculator as CALCULATE
from src.business import indicator as INDICATOR
# ----------------------------------------------------------------


# Basic Test Algorithms
def BASIC_DCA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, PER_TRANSACTION):
    algorithmName = "DCA"

    totalCoin = buyNum = sellNum = totalInvesment = 0
    coinSymbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 0)
    openPrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 1)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 4)

    sma25Length = S.MA_LENGTHS[0]
    sma25 = CALCULATE.SMA(coinSymbol, CANDLE_PERIOD, sma25Length)

    for i in range(len(closePrice)):
        if S.PD.isna(sma25[i]) is False:
            if closePrice[i - 1] < sma25[i - 1] and openPrice[i] > sma25[i]:
                print("####################################################")
                coin = CALCULATE.TEST_BUY(PER_TRANSACTION, closePrice[i])
                totalCoin += coin
                totalInvesment += PER_TRANSACTION
                buyNum += 1
                print(f"{coin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
    CALCULATE.TEST_PRINT_RESULT(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                                totalCoin, buyNum, sellNum, closePrice[len(closePrice)-1], totalInvesment)


def BASIC_GOLDENCROSS_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "Golden Cross"

    totalCoin = buyNum = sellNum = totalInvesment = 0
    coinSymbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 0)
    openPrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 1)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 4)

    sma50Length = S.MA_LENGTHS[1]
    sma200Length = S.MA_LENGTHS[2]
    sma50 = CALCULATE.SMA(coinSymbol, CANDLE_PERIOD, sma50Length)
    sma200 = CALCULATE.SMA(coinSymbol, CANDLE_PERIOD, sma200Length)

    for i in range(len(closePrice)):
        if S.PD.isna(sma50[i]) is False:
            if sma50[i - 1] < sma200[i - 1] and sma50[i] > sma200[i] and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, openPrice[i])
                WALLET = 0
                buyNum += 1
                print(f"{totalCoin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if sma50[i - 1] > sma200[i - 1] and sma50[i] < sma200[i] and totalCoin != 0:
                print(f"{totalCoin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, openPrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_PRINT_RESULT(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                                totalCoin, buyNum, sellNum, closePrice[len(closePrice)-1], totalInvesment)


def BASIC_STOCHRSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    algorithmName = "Basic StochRSI"

    totalCoin = buyNum = sellNum = totalInvesment = 0
    coinSymbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)
    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 0)
    openPrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 1)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, None, 4)

    stochRSI = INDICATOR.STOCHRSI(coinSymbol, CANDLE_PERIOD)
    stochRSI_K = stochRSI["stochRSI_K"]

    for i in range(len(closePrice)):
        if S.PD.isna(stochRSI_K[i]) is False:
            if (stochRSI_K[i] > 10 and stochRSI_K[i] < 30 or stochRSI_K[i] > 90) and WALLET != 0:
                print("####################################################")
                totalCoin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"STOCHRSI: {stochRSI_K[i]} - {totalCoin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if (stochRSI_K[i] > 70 and stochRSI_K[i] < 90 or stochRSI_K[i] < 10) and totalCoin != 0:
                print(f"STOCHRSI: {stochRSI_K[i]} - {totalCoin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(totalCoin, openPrice[i])
                totalCoin = 0
                sellNum += 1
                print("####################################################")
    CALCULATE.TEST_PRINT_RESULT(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, algorithmName, WALLET,
                                totalCoin, buyNum, sellNum, closePrice[len(closePrice)-1], totalInvesment)
# ----------------------------------------------------------------
