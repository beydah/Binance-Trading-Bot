# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import indicator as INDICATOR
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import message as MESSAGE
from src.engine.message import transactions as TRANSACTIONS
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# THREAD
from src.engine.thread import timer as TIMER
from src.engine.thread import debugger as DEBUGGER
from src.engine.thread import processor as PROCESSOR
# ----------------------------------------------------------------


def START():
    bot = LIB.TELEBOT(API.TELEGRAM_BOT_TOKEN)
    bot.set_update_listener(MESSAGE.GET)
    while True:
        try:
            bot.polling()
            break
        except Exception: MESSAGE.SEND_ERROR(f"Bot Start: {Exception}")
# ----------------------------------------------------------------
