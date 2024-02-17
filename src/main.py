# ----------------------------------------------------------------
# Added Links
from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
from src.engine import dataops as DATA
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import algotest as TEST
from src.engine import algotrade as TRADE
from src.business import business as BUSINESS
# ----------------------------------------------------------------
# Test Area
DATA.WRITE_FAVORITELIST()
'''
CALCULATE.SEND_MESSAGE("...TEST START...")
TEST.MIX_ALGORITHM("BTC", "USDT", "15m", 1000)
TEST.MIX_ALGORITHM("BTC", "USDT", "30m", 1000)
TEST.MIX_ALGORITHM("BTC", "USDT", "1h", 1000)
TEST.MIX_ALGORITHM("BTC", "USDT", "2h", 1000)
TEST.MIX_ALGORITHM("BTC", "USDT", "4h", 1000)
TEST.MIX_ALGORITHM("BTC", "USDT", "8h", 1000)
CALCULATE.SEND_MESSAGE(".....")
TEST.MIX_ALGORITHM("ID", "USDT", "15m", 1000)
TEST.MIX_ALGORITHM("ID", "USDT", "30m", 1000)
TEST.MIX_ALGORITHM("ID", "USDT", "1h", 1000)
TEST.MIX_ALGORITHM("ID", "USDT", "2h", 1000)
TEST.MIX_ALGORITHM("ID", "USDT", "4h", 1000)
TEST.MIX_ALGORITHM("ID", "USDT", "8h", 1000)
CALCULATE.SEND_MESSAGE(".....")
TEST.MIX_ALGORITHM("MULTI", "USDT", "15m", 1000)
TEST.MIX_ALGORITHM("MULTI", "USDT", "30m", 1000)
TEST.MIX_ALGORITHM("MULTI", "USDT", "1h", 1000)
TEST.MIX_ALGORITHM("MULTI", "USDT", "2h", 1000)
TEST.MIX_ALGORITHM("MULTI", "USDT", "4h", 1000)
TEST.MIX_ALGORITHM("MULTI", "USDT", "8h", 1000)
CALCULATE.SEND_MESSAGE(".....")
TEST.MIX_ALGORITHM("XEC", "USDT", "15m", 1000)
TEST.MIX_ALGORITHM("XEC", "USDT", "30m", 1000)
TEST.MIX_ALGORITHM("XEC", "USDT", "1h", 1000)
TEST.MIX_ALGORITHM("XEC", "USDT", "2h", 1000)
TEST.MIX_ALGORITHM("XEC", "USDT", "4h", 1000)
TEST.MIX_ALGORITHM("XEC", "USDT", "8h", 1000)
CALCULATE.SEND_MESSAGE(".....")
TEST.MIX_ALGORITHM("AGIX", "USDT", "15m", 1000)
TEST.MIX_ALGORITHM("AGIX", "USDT", "30m", 1000)
TEST.MIX_ALGORITHM("AGIX", "USDT", "1h", 1000)
TEST.MIX_ALGORITHM("AGIX", "USDT", "2h", 1000)
TEST.MIX_ALGORITHM("AGIX", "USDT", "4h", 1000)
TEST.MIX_ALGORITHM("AGIX", "USDT", "8h", 1000)
CALCULATE.SEND_MESSAGE("...TEST END...")
TEST.DCA_ALGORITHM("BTC", "USDT", "1h", 1000)
TEST.EMA_ALGORITHM("BTC", "USDT", "1h", 1000)
TEST.GOLDENCROSS_ALGORITHM("BTC", "USDT", "1h", 1000)
TEST.RSI_ALGORITHM("BTC", "USDT", "1h", 1000)
TEST.STOCHRSI_ALGORITHM("BTC", "USDT", "1h", 1000)
TEST.MIX_ALGORITHM("BTC", "USDT", "1h", 1000)
'''
# ----------------------------------------------------------------
