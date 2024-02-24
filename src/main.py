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
def ALGOTEST_MIX():
    coin = ["BTC", "ETH", "BNB", "SOL", "XRP"]
    rightSymbol = "USDT"
    wallet = 1000
    CALCULATE.SEND_MESSAGE(".....TEST START.....")
    # DATA.WRITE_FAVORITELIST()
    for i in range(5):
        for j in range(5):
            TEST.GOLDENCROSS_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.DCA_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.EMA_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.RSI_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.STOCHRSI_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.MIX_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            if j < 4: CALCULATE.SEND_MESSAGE(".....NEXT PERIOD.....")
        '''
        '''
        TEST.PERIOD_ALGORITHM(coin[i], rightSymbol, wallet)
        if i < 4: CALCULATE.SEND_MESSAGE(".....NEXT COIN.....")
    CALCULATE.SEND_MESSAGE(".....TEST END.....")


ALGOTEST_MIX()
print(CALCULATE.TOTAL_WALLET())
# ----------------------------------------------------------------
