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
# ----------------------------------------------------------------


# Test Area
def ALGOTEST():
    CALCULATE.SEND_MESSAGE(".....TEST START.....")
    # Test 1
    '''
    test = DATA.READ_WALLET()
    CALCULATE.SEND_MESSAGE(test)
    test = DATA.READ_WALLET(COIN="LDUSDT")
    CALCULATE.SEND_MESSAGE(test)
    for i in range(3): CALCULATE.SEND_MESSAGE(DATA.READ_WALLET(HEAD_ID=i))
    for i in range(3): CALCULATE.SEND_MESSAGE(DATA.READ_WALLET(COIN="LDUSDT", HEAD_ID=i))
    '''
    # Test 2
    '''
    DATA.WRITE_FAVORITELIST()
    '''
    # Test 3
    '''
    coin = ["BTC", "ETH", "BNB", "SOL", "XRP"]
    rightSymbol = "USDT"
    wallet = 1000
    for i in range(5):
        for j in range(5):
            TEST.DCA_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.EMA_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.GOLDENCROSS_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.RSI_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.STOCHRSI_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            TEST.GOLDENFIVE_ALGORITHM(coin[i], rightSymbol, DEF.CANDLE_PEROIDS[j], wallet)
            if j < 4: CALCULATE.SEND_MESSAGE(".....NEXT PERIOD.....")
        TEST.FIVEPERIOD_ALGORITHM(coin[i], rightSymbol, wallet)
        if i < 4: CALCULATE.SEND_MESSAGE(".....NEXT COIN.....")
    '''
    DATA.WRITE_TOTAL_BALANCE()
    CALCULATE.SEND_MESSAGE(".....TEST END.....")


ALGOTEST()
# ----------------------------------------------------------------
