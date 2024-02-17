# ----------------------------------------------------------------
# Added Links
from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
from src.engine import dataops as DATA
# ----------------------------------------------------------------


# Test Calculations
def TEST_BUY(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY / WEALTH_PRICE
    commission = coinQuantity * DEF.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    return coinQuantity


def TEST_SELL(WEALTH_QUANTITY, WEALTH_PRICE):
    coinQuantity = WEALTH_QUANTITY * WEALTH_PRICE
    commission = coinQuantity * DEF.BINANCE_COMISSION_RATE
    coinQuantity -= commission
    return coinQuantity
# ----------------------------------------------------------------


# Message Calculations
def SEND_MESSAGE(BOT_MESSAGE):
    print(BOT_MESSAGE)
    URL = (f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
           f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
           f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    LIB.REQUEST.get(URL)


def TEST_MESSAGE(LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, ALGORITHM_NAME, WALLET,
                 TOTAL_COIN, BUY_NUM, SELL_NUM, CLOSE_PRICE, TOTAL_INVESMENT):
    message = (f"Algorithm: {ALGORITHM_NAME}\n"
               f"Symbol: {LEFT_SMYBOL + RIGHT_SYMBOL} - Period: {CANDLE_PERIOD}\n"
               f"Total Transactions: {BUY_NUM + SELL_NUM}\n"
               f"Total Investment: {TOTAL_INVESMENT} - {RIGHT_SYMBOL}\n")
    if TOTAL_COIN != 0:
        message += (f"Total Coin: {TOTAL_COIN} - {LEFT_SMYBOL}\n"
                    f"Current Wallet: {TOTAL_COIN * CLOSE_PRICE} - {RIGHT_SYMBOL}")
    else: message += f"Current Wallet: {WALLET} - {RIGHT_SYMBOL}"
    SEND_MESSAGE(message)
# ----------------------------------------------------------------


# Get Calculations
def GET_CHANGE_PERCENT(COIN_SYMBOL, DAYS):
    past = LIB.TD(days=DAYS)
    today = LIB.TIME.now()
    past_date = today - past
    today = today.strftime("%Y-%m-%d %H:%M:%S")
    past_date = past_date.strftime("%Y-%m-%d %H:%M:%S")
    try:
        temp = DATA.READ_CANDLE(COIN_SYMBOL, "1m", today, 1, 4)
        currentPrice = temp[len(temp) - 1]
        temp = DATA.READ_CANDLE(COIN_SYMBOL, "1m", past_date, 1, 4)
        pastPrice = temp[len(temp) - 1]
        priceDifference = currentPrice - pastPrice
        percentChange = round((priceDifference / pastPrice) * 100, 4)
    except Exception: percentChange = 0
    DATA.DELETE_CANDLE(COIN_SYMBOL, "1m")
    return percentChange


def GET_MINLIST():
    df = DATA.READ_CHANGELIST()
    minAVGList = LIB.HEAP.nsmallest(5, df["AVG_Percent"])
    minCoinList = df.loc[df["AVG_Percent"].isin(minAVGList), ["Coin_Symbol", "AVG_Percent"]]
    df_minCoinList = minCoinList.sort_values("AVG_Percent")
    SEND_MESSAGE(f"Favorite List: \n{minCoinList}")

    maxAVGList = LIB.HEAP.nlargest(5, df["AVG_Percent"])
    maxCoinList = df.loc[df["AVG_Percent"].isin(maxAVGList), ["Coin_Symbol", "AVG_Percent"]]
    SEND_MESSAGE(f"Alert List: \n{maxCoinList}")

    return df_minCoinList["Coin_Symbol"]


def GET_SYMBOL_FROM_ID(SYMBOL_ID):
    filePath = LIB.OS.path.join("../.data", f"FAVORITELIST.csv")
    if LIB.OS.path.exists(filePath) is False: DATA.WRITE_FAVORITECOINS()
    with open(filePath, "r", newline="") as csvFile:
        headers = ["Coin_Symbol"]
        df = LIB.PD.read_csv(filePath, names=headers)
    csvFile.close()
    favorite_coins = df["Coin_Symbol"].tolist()
    return favorite_coins[SYMBOL_ID]


def GET_PERIOD_FROM_ID(PERIOD_ID): return DEF.CANDLE_PEROIDS[PERIOD_ID]
# ----------------------------------------------------------------
