from src.business import business as B
from src.business import calculator as C
from src.settings import settings as S


def DCA_ALGORITHM(SMYBOL_ID, PERIOD_ID, DOLLAR_PER_TRANSACTION):
    try:
        purchasesNum = 0
        totalCoin = 0
        commission = 0
        commissionRate = 1 / 10

        symbol = S.COIN_SYMBOLS[SMYBOL_ID]
        openTime = B.RETURN_CANDLE_SYMBOLS(SMYBOL_ID, PERIOD_ID, 0)
        closePrice = B.RETURN_CANDLE_SYMBOLS(SMYBOL_ID, PERIOD_ID, 4)

        sma = C.MA(SMYBOL_ID, PERIOD_ID)

        for i in range(len(closePrice)):
            if B.PD.isna(sma[i]) is False:
                if closePrice[i - 1] < sma[i - 1] and closePrice[i] > sma[i]:
                    print(DOLLAR_PER_TRANSACTION / closePrice[i], " ", symbol, " Received on ", openTime[i + 1])
                    print("####################################################")
                    purchasesNum += 1
                    totalCoin += DOLLAR_PER_TRANSACTION / closePrice[i]
                    commission += commissionRate * DOLLAR_PER_TRANSACTION

        print("Total Transactions: ", purchasesNum)
        print("Total Received ", symbol, ": ", totalCoin)
        print("Total Investment: ", purchasesNum * DOLLAR_PER_TRANSACTION, " Dollar")
        print("Current Wallet: ", totalCoin * closePrice[len(closePrice) - 1] - commission, " Dollar")
    except Exception:
        print("ERROR - TEST_DCA_ALGORITHM: Couldn't Test DCA Algorithm")
        return -1
