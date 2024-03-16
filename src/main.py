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
from src.engine.message import bot as BOT
from src.engine.message import message as MESSAGE
from src.engine.message import transactions as TRANSACTIONS
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------
MESSAGE.SEND(".....START.....")
if any([API.TELEGRAM_BOT_TOKEN, API.TELEGRAM_USER_ID, API.BINANCE_KEY]): BOT.START()
else: MESSAGE.SEND_ERROR("API Keys are missing!")
MESSAGE.SEND(".....END.....")
# ----------------------------------------------------------------
