# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import message as MSG
from src.engine.message import transactions as T
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
# ----------------------------------------------------------------


def START():
    bot = LIB.TELEBOT(API.Telegram_Bot_Token)
    bot.set_update_listener(MSG.GET)
    while True:
        try: bot.polling()
        except Exception as e: MSG.SEND_ERROR(f"Bot Start: {e}")


def PROCESSOR():
    date = LIB.DATE.datetime.now()
    while True:
        now = LIB.DATE.datetime.now()
        # if date.strftime("%d") != now.strftime("%d"):
        # TODO: TEST THIS
        if date.strftime("%H") != now.strftime("%H"):
            MSG.SEND("New Day Protocol Start")
            date = now
            WRITE.WALLET_CHANGES()
            T.Transaction_Lock[T.ANALYSIS_WALLET] = True
            CALCULATE.WALLET_INFO()
            T.Transaction_Lock[T.ANALYSIS_WALLET] = False
            T.Transaction_Lock[T.ANALYSIS_COIN_LIST] = T.Transaction_Lock[T.WRITE_COIN_LIST] = True
            T.Transaction_Lock[T.INSERT_COIN_LIST] = T.Transaction_Lock[T.DROP_COIN_LIST] = True
            DATA.GET_COINLIST_INFO()
            T.Transaction_Lock[T.ANALYSIS_COIN_LIST] = T.Transaction_Lock[T.WRITE_COIN_LIST] = False
            T.Transaction_Lock[T.INSERT_COIN_LIST] = T.Transaction_Lock[T.DROP_COIN_LIST] = False
            MSG.SEND("New Day Protocol End")
        LIB.TIME.sleep(1000)
# ----------------------------------------------------------------
