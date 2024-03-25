# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import read as READ
from src.engine.data import write as WRITE
# MATH
from src.engine.trade import calculator as CALCULATE
from src.engine.trade import indicator as INDICATOR
# MESSAGE
from src.engine.bot import message as MSG
from src.engine.bot import transactions as T
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def BEYZA_STOP():
    T.Transaction[T.Trade] = False
    while True:
        if T.Transaction[T.Wallet]: LIB.TIME.sleep(125)
        else: break
    wallet = READ.WALLET()
    if not wallet.empty:
        headers = [DEF.Wallet_Headers[0], DEF.Wallet_Headers[1], DEF.Wallet_Headers[2]]
        for i in range(len(wallet[headers[0]])):
            if T.Transaction[T.Trade]: return None
            if wallet[headers[0]][i][:2] == "LD" or wallet[headers[0]][i] == "USDT": continue
            if wallet[headers[2]][i] <= DEF.MIN_USDT_Balance: continue
            CALCULATE.DELETE_STOP_LOSS(wallet[headers[0]][i])
            CALCULATE.MARKET_SELL(Coin=wallet[headers[0]][i], Quantity=wallet[headers[1]][i])
    MSG.SEND("Trade Bot Stop")


def BEYZA_START():
    T.Transaction[T.Trade] = True
    MSG.SEND("Trade Bot Start")
    while True:
        if not T.Transaction[T.Trade]: return None
        headers = [DEF.Wallet_Headers[0], DEF.Wallet_Headers[1], DEF.Wallet_Headers[2]]
        # ----------------------------------------------------------------
        while True:
            if T.Transaction[T.Wallet]: LIB.TIME.sleep(125)
            else: break
        wallet = READ.WALLET()
        if not wallet.empty:
            for i in range(len(wallet[headers[0]])):
                if not T.Transaction[T.Trade]: return None
                if wallet[headers[0]][i][:2] == "LD" or wallet[headers[0]][i] == "USDT": continue
                if wallet[headers[2]][i] <= DEF.MIN_USDT_Balance: continue
                # ----------------------------------------------------------------
                prices = READ.CANDLE(Coin=wallet[headers[0]][i], Period=DEF.Candle_Periods[4], Limit=205, Head_ID=4)
                if len(prices) < 205:
                    MSG.SEND(f"I Cannot Sell {wallet[headers[0]][i]} Because is Still New")
                    WRITE.DROP_FAVORITELIST(wallet[headers[0]][i])
                    continue
                if INDICATOR.GOLDEN_FIVE_SIGNAL(INDICATOR.GOLDEN_FIVE(prices)) == 1: continue
                # ----------------------------------------------------------------
                prices = READ.CANDLE(Coin=wallet[headers[0]][i], Limit=205, Head_ID=4)
                if INDICATOR.GOLDEN_FIVE_SIGNAL(INDICATOR.GOLDEN_FIVE(prices)) != -1: continue
                CALCULATE.DELETE_STOP_LOSS(wallet[headers[0]][i])
                CALCULATE.MARKET_SELL(Coin=wallet[headers[0]][i], Quantity=wallet[headers[1]][i])
        # ----------------------------------------------------------------
        while True:
            if T.Transaction[T.Coinlist]: LIB.TIME.sleep(125)
            else: break
        favoriteList = READ.FAVORITELIST()
        if not favoriteList.empty:
            for coin in favoriteList[headers[0]]:
                if not T.Transaction[T.Trade]: return None
                USDT_Balance = READ.WALLET(Coin="USDT", Head_ID=2)
                if USDT_Balance.empty or USDT_Balance.item() / 2 <= DEF.MIN_USDT_Balance: continue
                USDT = USDT_Balance.item() / 2
                # ----------------------------------------------------------------
                prices = READ.CANDLE(Coin=coin, Period=DEF.Candle_Periods[4], Limit=205, Head_ID=4)
                if len(prices) < 205:
                    MSG.SEND(f"I Cannot Buy {coin} Because is Still New")
                    WRITE.DROP_FAVORITELIST(coin)
                    continue
                if INDICATOR.GOLDEN_FIVE_SIGNAL(INDICATOR.GOLDEN_FIVE(prices)) == -1: continue
                # ----------------------------------------------------------------
                prices = READ.CANDLE(Coin=coin, Limit=205, Head_ID=4)
                if INDICATOR.GOLDEN_FIVE_SIGNAL(INDICATOR.GOLDEN_FIVE(prices)) != 1: continue
                prices = READ.CANDLE(Coin=coin, Period="1m", Limit=1, Head_ID=4)
                quantity = DATA.FIND_COIN_QUANTITY(USDT_Quantity=USDT, Coin_Price=prices[len(prices)-1])
                trade = CALCULATE.MARKET_BUY(Coin=coin, Quantity=quantity)
                if not trade: continue
                CALCULATE.DELETE_STOP_LOSS(coin)
                CALCULATE.STOP_LOSS(coin)
        # ----------------------------------------------------------------
        if T.Transaction[T.Trade]: MSG.SEND("Trade Bot Wait")
        LIB.TIME.sleep(500)
        if T.Transaction[T.Trade]: MSG.SEND("Trade Bot Restart")
# ----------------------------------------------------------------


def BEYZA_BACKTEST(Coin, Period, Wallet, Monthly_Addition):
    time = READ.CANDLE(Coin=Coin, Period=Period, Head_ID=0)
    time_format = LIB.DATE.datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S")
    old_month = time_format.strftime("%m")
    first_transaction_date = time[len(time)-1]
    last_transaction_date = time[0]
    total_coin = buy_num = sell_num = 0
    total_invesment = entry_wallet = Wallet
    # ----------------------------------------------------------------
    prices = READ.CANDLE(Coin=Coin, Period=Period, Head_ID=4)
    ema25 = INDICATOR.EMA(MA_Length=DEF.MA_Lengths[0], Prices=prices)
    sma25 = INDICATOR.SMA(MA_Length=DEF.MA_Lengths[0], Prices=prices)
    sma50 = INDICATOR.SMA(MA_Length=DEF.MA_Lengths[1], Prices=prices)
    sma200 = INDICATOR.SMA(MA_Length=DEF.MA_Lengths[2], Prices=prices)
    rsi = INDICATOR.RSI(prices)
    stoch_RSI = INDICATOR.STOCH_RSI(prices)
    for i in range(len(time)):
        # ----------------------------------------------------------------
        time_format = LIB.DATE.datetime.strptime(time[i], "%Y-%m-%d %H:%M:%S")
        if time_format.strftime("%m") != old_month:
            old_month = time_format.strftime("%m")
            Wallet += Monthly_Addition
            total_invesment += Monthly_Addition
        # ----------------------------------------------------------------
        if not any(LIB.PD.isna([stoch_RSI[i], rsi[i], sma50[i], sma25[i]])):
            golden_nums = INDICATOR.GOLDEN_FIVE_TEST(prices[i - 2], prices[i - 1], ema25[i-2], ema25[i-1],
                                                     sma25[i - 2], sma25[i - 1], sma50[i-2], sma50[i-1],
                                                     sma200[i-2], sma200[i-1], rsi[i-1], stoch_RSI[i-1])
            signal = INDICATOR.GOLDEN_FIVE_SIGNAL(golden_nums)
            if signal == 1 or signal == -1:
                # ----------------------------------------------------------------
                if time[i] < first_transaction_date: first_transaction_date = time[i]
                if time[i] > last_transaction_date: last_transaction_date = time[i]
                # ----------------------------------------------------------------
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
                # ----------------------------------------------------------------
    MSG.SEND_TEST(Coin, Period, first_transaction_date, last_transaction_date, buy_num, sell_num,
                  entry_wallet, Monthly_Addition, total_invesment, total_coin, prices[len(prices) - 1], Wallet)
# ----------------------------------------------------------------
