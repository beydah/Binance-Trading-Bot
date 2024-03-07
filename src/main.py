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
# THREAD
from src.engine.thread import timer as TIMER
from src.engine.thread import debugger as DEBUGGER
from src.engine.thread import processor as PROCESSOR
# ----------------------------------------------------------------


# Test Area
def TEST():
    MESSAGE.SEND(".....TEST START.....")
    """
    print(DATA.GET_BINANCE())
    print(DATA.GET_CANDLE("BTC", "8h"))
    print(DATA.GET_ACCOUNT())
    print(DATA.GET_BALANCES())
    print(DATA.GET_FULLCOIN())
    print(DATA.GET_USDT_BALANCE("BTC", 1))
    print(DATA.GET_TOTAL_WALLET(2))
    print(DATA.GET_WALLET_CHANGE(200,100,0))
    print(DATA.GET_COIN_CHANGE("BTCUSDT", 30))
    print(DATA.GET_COINLIST_INFO())
    print(DATA.GET_COIN_INFO("BNB"))
    print(DATA.GET_WALLET_INFO())
    print(DATA.GET_COIN_FROM_FAVORITELIST(0))
    print(DATA.FIND_COIN("BTC"))
    print(DATA.FIND_MINLIST())
    print(DATA.FIND_MAXLIST())
    TRADE.TEST("USDC")
    """
    BOT.START()
    '''
    '''
    MESSAGE.SEND(".....TEST END.....")


TEST()
# ----------------------------------------------------------------
