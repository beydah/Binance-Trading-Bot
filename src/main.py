# ----------------------------------------------------------------
# Added Links
from src.business import business as B
from src.business import calculator as CALCULATE
from src.business import indicator as INDICATOR
from src.business import backtest as TEST
from src.settings import settings as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Test Area
TEST.DCA_ALGORITHM("BTC", "USDT", "8h", 1000)
TEST.GOLDENCROSS_ALGORITHM("BTC", "USDT", "8h", 1000)
TEST.STOCHRSI_ALGORITHM("BTC", "USDT", "8h", 1000)
TEST.RSI_ALGORITHM("BTC", "USDT", "8h", 1000)
print(INDICATOR.STOCHRSI("BTCUSDT", "8h"))
print(INDICATOR.RSI("BTCUSDT", "8h"))
print(INDICATOR.MACD("BTCUSDT", "8h"))
print(INDICATOR.BOLL("BTCUSDT", "8h"))
print(INDICATOR.SMA("BTCUSDT", "8h", 25))
print(INDICATOR.EMA("BTCUSDT", "8h", 50))
B.WRITE_FAVORITELIST()
CALCULATE.SEND_MESSAGE(f"Top Favorites Coin: {CALCULATE.GET_SYMBOL_FROM_ID(0)}")
# ----------------------------------------------------------------
