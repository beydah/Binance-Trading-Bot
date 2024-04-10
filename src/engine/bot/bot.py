# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import read as READ
from src.engine.data import write as WRITE
# MATH
from src.engine.trade import calculator as CALCULATE
from src.engine.trade import trade as TRADE
# MESSAGE
from src.engine.bot import message as MSG
from src.engine.bot import transactions as T
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def START():
    bot = LIB.TELEBOT(API.Telegram_Bot_Token)
    bot.set_update_listener(MSG.GET)
    while True:
        try: bot.polling()
        except Exception as e: MSG.SEND_ERROR(f"START: {e}")


def PROCESSOR():
    date = LIB.DATE.datetime.now()
    while True:
        now = LIB.DATE.datetime.now()
        if date.strftime("%H") != now.strftime("%H"):
            if date.strftime("%d") != now.strftime("%d"):
                while True:
                    if T.Transaction[T.Wallet]: LIB.TIME.sleep(250)
                    else: break
                MSG.SEND("New Day Protocol Start")
                WRITE.WALLET_CHANGES()
                CALCULATE.WALLET_CHANGES_INFO()
            while True:
                if T.Transaction[T.Coinlist]: LIB.TIME.sleep(250)
                else: break
            MSG.SEND("New Hour Protocol Start")
            WRITE.COINLIST_CHANGES()
            WRITE.FAVORITELIST()
            date = now
        LIB.TIME.sleep(1000)


def BACKTESTER(Prompt):
    T.Transaction[T.Coin] = True
    Prompt = Prompt.replace(" ", "")
    coin = entry_wallet = monthly_addition = None
    if "," in Prompt:
        if Prompt.count(",") == 1: coin, entry_wallet = Prompt.split(",")
        elif Prompt.count(",") == 2: coin, entry_wallet, monthly_addition = Prompt.split(",")
    else: coin = Prompt
    if CALCULATE.FIND_COIN(coin):
        prices = READ.CANDLE(Coin=coin, Period=DEF.Candle_Periods[4], Head_ID=4)
        if len(prices) < 205: MSG.SEND(f"I cannot test because {coin} is still very new.")
        else:
            try: entry_wallet = int(entry_wallet)
            except Exception: entry_wallet = 1000
            try: monthly_addition = int(monthly_addition)
            except Exception: monthly_addition = 100
            for period in DEF.Candle_Periods: TRADE.BEYZA_BACKTEST(coin, period, entry_wallet, monthly_addition)
    T.Transaction[T.Coin] = False
# ----------------------------------------------------------------
