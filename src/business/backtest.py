from src.business import calculator as CALCULATE
from src.business import business as B
from src.settings import settings as S


def DCA_ALGORITHM(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, PER_TRANSACTION):
    symbol = B.COMBINE_SYMBOL(LEFT_SMYBOL, RIGHT_SYMBOL)

    purchasesNum = 0
    totalCoin = 0
    commission = 0

    openTime = B.READ_CANDLE(symbol, CANDLE_PERIOD, 0)
    closePrice = B.READ_CANDLE(symbol, CANDLE_PERIOD, 4)

    sma25 = CALCULATE.SMA(symbol, CANDLE_PERIOD, 25)

    for i in range(len(closePrice)):
        if B.PD.isna(sma25[i]) is False:
            if closePrice[i - 1] < sma25[i - 1] and closePrice[i] > sma25[i]:
                print("####################################################")
                print(f"{PER_TRANSACTION / closePrice[i]} - {LEFT_SMYBOL} - BUY - {openTime[i + 1]}")
                totalCoin += PER_TRANSACTION / closePrice[i]
                commission += S.BINANCE_COMISSION_RATE * PER_TRANSACTION
                purchasesNum += 1

    print("####################################################")
    print(f"Total Transactions: {purchasesNum}")
    print(f"Total Received: {symbol} {totalCoin}")
    print(f"Total Investment: {purchasesNum * PER_TRANSACTION} {RIGHT_SYMBOL}")
    print(f"Current Wallet: {totalCoin * closePrice[len(closePrice) - 1] - commission} {RIGHT_SYMBOL}")
    print("####################################################")
