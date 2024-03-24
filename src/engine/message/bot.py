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
        if date.strftime("%H") != now.strftime("%H"):
            if date.strftime("%d") != now.strftime("%d"):
                while True:
                    if not T.Transaction[T.Coinlist] and not T.Transaction[T.Wallet]:
                        MSG.SEND("New Day Protocol Start")
                        WRITE.COINLIST_CHANGES()
                        WRITE.FAVORITELIST()
                        WRITE.WALLET_CHANGES()
                        CALCULATE.WALLET_CHANGES_INFO()
                        MSG.SEND("New Day Protocol End")
                        break
                    else: LIB.TIME.sleep(250)
            else:
                while True:
                    if not T.Transaction[T.Coinlist] and not T.Transaction[T.Wallet]:
                        MSG.SEND("New Hour Protocol Start")
                        WRITE.COINLIST_CHANGES()
                        WRITE.FAVORITELIST()
                        MSG.SEND("New Hour Protocol End")
                        break
                    else: LIB.TIME.sleep(250)
            date = now
        LIB.TIME.sleep(1000)
# ----------------------------------------------------------------
