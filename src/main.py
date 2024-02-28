# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import wallet as WALLET
from src.dataops import list as LIST
from src.dataops import message as MESSAGE

from src.engine import algotest as TEST
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR

from src.settings import settings as DEF
from src.settings import api as API
# ----------------------------------------------------------------


# Test Area
def ALGOTEST():
    MESSAGE.SEND(".....TEST START.....")
    # Test 1
    '''
    test = WALLET.READ()
    MESSAGE.SEND(test)
    test = WALLET.READ(COIN="LDUSDT")
    MESSAGE.SEND(test)
    for i in range(3): MESSAGE.SEND(WALLET.READ(HEAD_ID=i))
    for i in range(3): MESSAGE.SEND(WALLET.READ(COIN="LDUSDT", HEAD_ID=i))
    '''
    # Test 2
    # LIST.WRITE_FAVORITE()
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
            if j < 4: MESSAGE.SEND(".....NEXT PERIOD.....")
        TEST.FIVEPERIOD_ALGORITHM(coin[i], rightSymbol, wallet)
        if i < 4: MESSAGE.SEND(".....NEXT COIN.....")
    '''
    print(WALLET.READ())
    WALLET.WRITE_TOTAL_BALANCE()
    MESSAGE.SEND(".....TEST END.....")


ALGOTEST()
# ----------------------------------------------------------------
