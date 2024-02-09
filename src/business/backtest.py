from src.business import calculator as CALCULATE
from src.business import business as B
from src.settings import settings as S


def DCA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, PER_TRANSACTION):
    coinSymbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)

    buyNum = 0
    totalInvesment = 0
    totalCoin = 0

    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 0)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 4)

    sma25Length = S.MA_LENGTHS[0]
    sma25 = CALCULATE.SMA(coinSymbol, CANDLE_PERIOD, sma25Length)

    for i in range(len(closePrice)):
        if B.PD.isna(sma25[i]) is False:
            if closePrice[i - 1] < sma25[i - 1] and closePrice[i] > sma25[i]:
                print("####################################################")
                coin = CALCULATE.TEST_BUY(PER_TRANSACTION, closePrice[i])
                totalCoin += coin
                totalInvesment += PER_TRANSACTION
                buyNum += 1
                print(f"{coin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")

    print("####################################################")
    print(f"Total Transactions: {buyNum}")
    print(f"Total Investment: {totalInvesment} - {RIGHT_SYMBOL}")
    print(f"Total Coin: {totalCoin} - {LEFT_SMYBOL}")
    print(f"Current Wallet: {totalCoin * closePrice[len(closePrice) - 1]} - {RIGHT_SYMBOL}")
    print("####################################################")


def GOLDEN_CROSS_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    coinSymbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)

    coin = 0
    buyNum = 0
    sellNum = 0

    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 0)
    openPrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 1)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 4)

    sma50Length = S.MA_LENGTHS[1]
    sma200Length = S.MA_LENGTHS[2]
    sma50 = CALCULATE.SMA(coinSymbol, CANDLE_PERIOD, sma50Length)
    sma200 = CALCULATE.SMA(coinSymbol, CANDLE_PERIOD, sma200Length)

    for i in range(len(closePrice)):
        if B.PD.isna(sma50[i]) is False:
            if sma50[i - 1] < sma200[i - 1] and sma50[i] > sma200[i] and WALLET != 0:
                print("####################################################")
                coin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"{coin} - {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if sma50[i - 1] > sma200[i - 1] and sma50[i] < sma200[i] and coin != 0:
                print(f"{coin} - {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(coin, openPrice[i])
                coin = 0
                sellNum += 1
                print("####################################################")
    print("####################################################")
    print(f"Total Transactions: {buyNum + sellNum}")
    print(f"Total Coin: {coin} - {LEFT_SMYBOL}")
    print(f"Total Coin ({RIGHT_SYMBOL}): {coin * closePrice[len(closePrice) - 1]} - {LEFT_SMYBOL}")
    print(f"Wallet: {WALLET} - {RIGHT_SYMBOL}")
    print("####################################################")


def BASIC_STOCHRSI_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, WALLET):
    coinSymbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)

    coin = 0
    buyNum = 0
    sellNum = 0

    openTime = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 0)
    openPrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 1)
    closePrice = B.READ_CANDLE(coinSymbol, CANDLE_PERIOD, 4)

    stochRSI = CALCULATE.STOCHRSI(coinSymbol, CANDLE_PERIOD)
    stochRSI_K = stochRSI["stochRSI_K"]

    for i in range(len(closePrice)):
        if B.PD.isna(stochRSI_K[i]) is False:
            if (stochRSI_K[i] > 10 and stochRSI_K[i] < 30 or stochRSI_K[i] > 90) and WALLET != 0:
                print("####################################################")
                coin = CALCULATE.TEST_BUY(WALLET, closePrice[i])
                WALLET = 0
                buyNum += 1
                print(f"STOCHRSI: {stochRSI_K[i]} - {coin} {LEFT_SMYBOL} - BUY - {openTime[i]}")
            if (stochRSI_K[i] > 70 and stochRSI_K[i] < 90 or stochRSI_K[i] < 10) and coin != 0:
                print(f"STOCHRSI: {stochRSI_K[i]} - {coin} {LEFT_SMYBOL} - SELL - {openTime[i]}")
                WALLET = CALCULATE.TEST_SELL(coin, openPrice[i])
                coin = 0
                sellNum += 1
                print("####################################################")
    print("####################################################")
    print(f"Total Transactions: {buyNum + sellNum}")
    print(f"Total Coin: {coin} - {LEFT_SMYBOL}")
    print(f"Total Coin: {coin * closePrice[len(closePrice) - 1]} - {RIGHT_SYMBOL}")
    print(f"Wallet: {WALLET} - {RIGHT_SYMBOL}")
    print("####################################################")
