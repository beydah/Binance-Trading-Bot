# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import message as MESSAGE
from src.engine.message import transactions as T
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
# ----------------------------------------------------------------


def START():
    bot = LIB.TELEBOT(API.TELEGRAM_BOT_TOKEN)
    bot.set_update_listener(MESSAGE.GET)
    while True:
        try: bot.polling()
        except Exception as e: MESSAGE.SEND_ERROR(f"Bot Start: {e}")


def PROCESSOR():
    date = LIB.DATE.datetime.now()
    while True:
        now = LIB.DATE.datetime.now()
        if date.strftime("%d") != now.strftime("%d"):
            MESSAGE.SEND("I started new day protocol...")
            date = now
            WRITE.WALLET_CHANGES()
            WRITE.COINLIST_CHANGES()
            WRITE.FAVORITELIST()
            T.TRANSACTION_LOCK[T.ANALYSIS_WALLET] = True
            CALCULATE.WALLET_INFO()
            T.TRANSACTION_LOCK[T.ANALYSIS_WALLET] = False
            T.TRANSACTION_LOCK[T.ANALYSIS_COIN_LIST] = T.TRANSACTION_LOCK[T.WRITE_COIN_LIST] = True
            T.TRANSACTION_LOCK[T.INSERT_COIN_LIST] = T.TRANSACTION_LOCK[T.DROP_COIN_LIST] = True
            DATA.GET_COINLIST_INFO()
            T.TRANSACTION_LOCK[T.ANALYSIS_COIN_LIST] = T.TRANSACTION_LOCK[T.WRITE_COIN_LIST] = False
            T.TRANSACTION_LOCK[T.INSERT_COIN_LIST] = T.TRANSACTION_LOCK[T.DROP_COIN_LIST] = False
            MESSAGE.SEND("New day protocol finished.")
        LIB.TIME.sleep(900)
# ----------------------------------------------------------------
