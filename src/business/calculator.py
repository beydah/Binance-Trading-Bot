# Added Pages
from src.settings import settings as S
from src.business import business as B


# ----------------------------------------------------------------


# Test Calculations
def TEST_BUY(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY / WEALTH_PRICE
    commission = coinQuantity * S.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    return coinQuantity


def TEST_SELL(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY * WEALTH_PRICE
    commission = coinQuantity * S.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    return coinQuantity


def TEST_PRINT_RESULT(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, ALGORITHM_NAME, WALLET,
                      TOTAL_COIN, BUY_NUM, SELL_NUM, CLOSE_PRICE, TOTAL_INVESMENT=None):
    message = (f"Algorithm: {ALGORITHM_NAME}\n"
               f"Symbol: {LEFT_SMYBOL + RIGHT_SYMBOL} - Period: {CANDLE_PERIOD}\n"
               f"Total Transactions: {BUY_NUM + SELL_NUM}\n")
    if TOTAL_INVESMENT is not None or 0: message += f"Total Investment: {TOTAL_INVESMENT} - {RIGHT_SYMBOL}\n"
    if TOTAL_COIN != 0:
        message += (f"Total Coin: {TOTAL_COIN} - {LEFT_SMYBOL}\n"
                    f"Current Wallet: {TOTAL_COIN * CLOSE_PRICE} - {RIGHT_SYMBOL}")
    else: message += f"Current Wallet: {WALLET} - {RIGHT_SYMBOL}"

    B.SEND_MESSAGE(message)
    print("####################################################")
    print(message)
    print("####################################################")


# ----------------------------------------------------------------


# Other Calculations
def CHANGE_PERCENT(COIN_SYMBOL, DAYS):
    past = S.TD(days=DAYS)

    today = S.TIME.now()
    past_date = today - past
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    past_date = past_date.strftime("%Y-%m-%d %H:%M:%S")

    try:
        temp = B.READ_CANDLE(COIN_SYMBOL, "1m", today, 1, 4)
        currentPrice = temp[len(temp) - 1]
        temp = B.READ_CANDLE(COIN_SYMBOL, "1m", past_date, 1, 4)
        pastPrice = temp[len(temp) - 1]
        priceDifference = currentPrice - pastPrice
        percentChange = round((priceDifference / pastPrice) * 100, 4)
    except Exception: percentChange = 0

    B.DELETE_CANDLE(COIN_SYMBOL, "1m")
    return percentChange


def FIND_MINIMUMLIST():
    df = B.READ_CHANGELIST()

    minimumAVGList = S.HEAP.nsmallest(5, df["AVG_Percent"])
    minimumCoinList = df.loc[df["AVG_Percent"].isin(minimumAVGList), ["Coin_Symbol", "AVG_Percent"]]
    df_minimumCoinList = minimumCoinList.sort_values("AVG_Percent")

    return df_minimumCoinList["Coin_Symbol"]
# ----------------------------------------------------------------
