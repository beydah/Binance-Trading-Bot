# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import bot as BOT
from src.engine.message import message as MSG
from src.engine.message import transactions as T
# SETTINGS
from src.engine.settings import api as API
from src.engine.settings import settings as DEF
from src.engine.settings import library as LIB
# ----------------------------------------------------------------


def MAIN():
    if any([API.Telegram_Bot_Token, API.Telegram_User_ID, API.Binance_Key, API.Binance_Secret]):
        MSG.SEND(DEF.Install_Message)
        # ----------------------------------------------------------------
        bot = LIB.THREAD(target=BOT.START)
        bot.start()
        # ----------------------------------------------------------------
        processor = LIB.THREAD(target=BOT.PROCESSOR)
        processor.start()
        # ----------------------------------------------------------------
        trade_stop = LIB.THREAD(target=TRADE.BEYZA_STOP)
        trade_stop.start()
        # ----------------------------------------------------------------
        WRITE.COINLIST_CHANGES()
        WRITE.WALLET_CHANGES()
        # ----------------------------------------------------------------
        MSG.SEND(DEF.Start_Message)
    else: MSG.SEND("API Keys are Missing!")


MAIN()
# ----------------------------------------------------------------
