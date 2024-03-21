# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
from src.engine.data import write as WRITE
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import indicator as INDICATOR
# MESSAGE
from src.engine.message import message as MSG
from src.engine.message import transactions as T
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


# Trader
def BEYZA_STOP():
    if T.Trade_Stop[0] is False: return None
    wallet = READ.WALLET()
    if not wallet.empty:
        for i in range(len(wallet["Coin"])):
            if T.Trade_Stop[0] is False: return None
            if (wallet["Coin"][i][:2] == "LD" or wallet["Coin"][i] == "USDT"
                or wallet["USDT Balance"][i] <= DEF.MIN_USDT_Balance): continue
            CALCULATE.DELETE_STOP_LOSS(wallet["Coin"][i])
            CALCULATE.MARKET_SELL(wallet["Coin"][i], wallet["Balance"][i])
    MSG.SEND("Trade Bot Stop")


def BEYZA_START():
    MSG.SEND("Trade Bot Start")
    while True:
        if T.Trade_Stop[0] is True: return None
        wallet = READ.WALLET()
        if not wallet.empty:
            for i in range(len(wallet["Coin"])):
                if T.Trade_Stop[0] is True: return None
                if (wallet["Coin"][i][:2] == "LD" or wallet["Coin"][i] == "USDT"
                    or wallet["USDT Balance"][i] <= DEF.MIN_USDT_Balance): continue
                prices = READ.CANDLE(Coin=wallet["Coin"][i], Limit=205, Head_ID=4)
                if len(prices) < 205:
                    MSG.SEND(f"I cannot sell {wallet['Coin'][i]} because is still very new.")
                    continue
                sma25 = INDICATOR.SMA(DEF.MA_Lengths[0], prices)
                ema25 = INDICATOR.EMA(DEF.MA_Lengths[0], prices)
                sma50 = INDICATOR.SMA(DEF.MA_Lengths[1], prices)
                sma200 = INDICATOR.SMA(DEF.MA_Lengths[2], prices)
                rsi = INDICATOR.RSI(prices)
                stochRSI = INDICATOR.STOCHRSI(prices)
                last = len(prices)-2
                if not any(LIB.PD.isna([stochRSI[last-1], rsi[last-1], sma200[last-1], sma50[last-1], sma25[last-1]])):
                    signal = INDICATOR.GOLDENFIVE_SIGNAL(
                        INDICATOR.GOLDENFIVE(prices[last-1], prices[last], sma25[last-1], sma25[last],
                                             sma50[last-1], sma50[last], sma200[last-1], sma200[last],
                                             ema25[last-1], ema25[last], rsi[last], stochRSI[last]))
                    if signal == -1:
                        CALCULATE.DELETE_STOP_LOSS(wallet["Coin"][i])
                        CALCULATE.MARKET_SELL(wallet["Coin"][i], wallet["Balance"][i])
        favoriteList = READ.FAVORITELIST()
        if not favoriteList.empty:
            for coin in favoriteList["Coin"]:
                if T.Trade_Stop[0] is True: return None
                USDTBalance = READ.WALLET(Coin="USDT", Head_ID=2)
                if USDTBalance.empty or USDTBalance.item() / 2 <= DEF.MIN_USDT_Balance: continue
                USDT = USDTBalance.item() / 2
                prices = READ.CANDLE(Coin=coin, Limit=205, Head_ID=4)
                if len(prices) < 205:
                    MSG.SEND(f"I cannot buy {coin} because is still very new.")
                    WRITE.DROP_FAVORITELIST(coin)
                    continue
                sma25 = INDICATOR.SMA(DEF.MA_Lengths[0], prices)
                ema25 = INDICATOR.EMA(DEF.MA_Lengths[0], prices)
                sma50 = INDICATOR.SMA(DEF.MA_Lengths[1], prices)
                sma200 = INDICATOR.SMA(DEF.MA_Lengths[2], prices)
                rsi = INDICATOR.RSI(prices)
                stochRSI = INDICATOR.STOCHRSI(prices)
                last = len(prices) - 2
                if not any(LIB.PD.isna([stochRSI[last-1], rsi[last-1], sma200[last-1], sma50[last-1], sma25[last-1]])):
                    signal = INDICATOR.GOLDENFIVE_SIGNAL(
                        INDICATOR.GOLDENFIVE(prices[last-1], prices[last], sma25[last-1], sma25[last],
                                             sma50[last-1], sma50[last], sma200[last-1], sma200[last],
                                             ema25[last-1], ema25[last], rsi[last], stochRSI[last]))
                    if signal == 1:
                        prices = READ.CANDLE(Coin=coin, Period="1m", Limit=1, Head_ID=4)
                        coin_quantity = DATA.FIND_COIN_QUANTITY(USDT, prices[len(prices)-1])
                        trade = CALCULATE.MARKET_BUY(coin, coin_quantity)
                        if trade: CALCULATE.CREATE_STOP_LOSS(coin)
        if not T.Trade_Stop[0]: MSG.SEND("Trade Bot Wait...")
        LIB.TIME.sleep(500)
        if not T.Trade_Stop[0]: MSG.SEND("Trade Bot Restart.")
# ----------------------------------------------------------------


# Tester
def TEST(PROMPT):
    PROMPT = PROMPT.replace(" ", "")
    coin = entry_wallet = monthly_addition = None
    if "," in PROMPT:
        if PROMPT.count(",") == 1: coin, entry_wallet = PROMPT.split(",")
        elif PROMPT.count(",") == 2: coin, entry_wallet, monthly_addition = PROMPT.split(",")
    else: coin = PROMPT
    try: entry_wallet = int(entry_wallet)
    except Exception: entry_wallet = 1000
    try: monthly_addition = int(monthly_addition)
    except Exception: monthly_addition = 100
    if CALCULATE.FIND_COIN(coin):
        prices = READ.CANDLE(Coin=coin, Period=DEF.Candle_Periods[4], Head_ID=4)
        if len(prices) < 205:
            MSG.SEND(f"I cannot test because {coin} is still very new.")
            return None
        for period in DEF.Candle_Periods: GOLDENFIVE(coin, period, entry_wallet, monthly_addition)


def GOLDENFIVE(Coin, Period, Wallet, Monthly_Addition):
    total_invesment = entry_wallet = Wallet
    total_coin = buy_num = sell_num = 0
    time = READ.CANDLE(Coin=Coin, Period=Period, Head_ID=0)
    prices = READ.CANDLE(Coin=Coin, Period=Period, Head_ID=4)
    sma25 = INDICATOR.SMA(DEF.MA_Lengths[0], prices)
    ema25 = INDICATOR.EMA(DEF.MA_Lengths[0], prices)
    sma50 = INDICATOR.SMA(DEF.MA_Lengths[1], prices)
    sma200 = INDICATOR.SMA(DEF.MA_Lengths[2], prices)
    rsi = INDICATOR.RSI(prices)
    stochRSI = INDICATOR.STOCHRSI(prices)
    time_format = LIB.DATE.datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S")
    old_month = time_format.strftime("%m")
    first_transaction_date = time[len(time)-1]
    last_transaction_date = time[0]
    for i in range(len(time)):
        time_format = LIB.DATE.datetime.strptime(time[i], "%Y-%m-%d %H:%M:%S")
        if time_format.strftime("%m") != old_month:
            old_month = time_format.strftime("%m")
            Wallet += Monthly_Addition
            total_invesment += Monthly_Addition
        if not any(LIB.PD.isna([stochRSI[i], rsi[i], sma50[i], sma25[i]])):
            signal = INDICATOR.GOLDENFIVE_SIGNAL(
                INDICATOR.GOLDENFIVE(prices[i-2], prices[i-1], sma25[i-2], sma25[i-1],
                                     sma50[i-2], sma50[i-1], sma200[i-2], sma200[i-1],
                                     ema25[i-2], ema25[i-1], rsi[i-1], stochRSI[i-1]))
            if signal == 1 or signal == -1:
                if time[i] < first_transaction_date: first_transaction_date = time[i]
                if time[i] > last_transaction_date: last_transaction_date = time[i]
                if signal == 1 and Wallet != 0:
                    print("####################################################")
                    total_coin += CALCULATE.TEST_BUY(Wallet, prices[i])
                    Wallet = 0
                    buy_num += 1
                    print(f"{total_coin} - {Coin} - BUY - {time[i]}")
                elif signal == -1 and total_coin != 0:
                    print(f"{total_coin} - {Coin} - SELL - {time[i]}")
                    Wallet += CALCULATE.TEST_SELL(total_coin, prices[i])
                    total_coin = 0
                    sell_num += 1
                    print("####################################################")
    MSG.SEND_TEST(Coin, Period, first_transaction_date, last_transaction_date, buy_num, sell_num,
                  entry_wallet, Monthly_Addition, total_invesment, total_coin, prices[len(prices) - 1], Wallet)
# ----------------------------------------------------------------
