# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import write as WRITE
# MESSAGE
from src.engine.bot import bot as BOT
from src.engine.bot import message as MSG
# SETTINGS
from src.engine.settings import api as API
from src.engine.settings import settings as DEF
from src.engine.settings import library as LIB
# ----------------------------------------------------------------


def MAIN():
    if any([API.Telegram_Bot_Token, API.Telegram_User_ID, API.Binance_Key, API.Binance_Secret]):
        MSG.SEND(DEF.Install_Message)
        # ----------------------------------------------------------------
        processor = LIB.THREAD(target=BOT.PROCESSOR)
        processor.start()
        # ----------------------------------------------------------------
        WRITE.WALLET_CHANGES()
        WRITE.COINLIST_CHANGES()
        # ----------------------------------------------------------------
        bot = LIB.THREAD(target=BOT.START)
        bot.start()
        # ----------------------------------------------------------------
        MSG.SEND(DEF.Start_Message)
    else: MSG.SEND("API Keys are Missing!")


MAIN()
# ----------------------------------------------------------------
