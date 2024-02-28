# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import wallet as WALLET

from src.engine import algotest as TEST
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Message Operations
def GET(): return


def SEND(BOT_MESSAGE):
    print(BOT_MESSAGE)
    try:
        URL = (f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
               f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
               f"&parse_mode=Markdown&text={BOT_MESSAGE}")
        LIB.REQUEST.get(URL)
    except Exception as e: print(f"Error: {e}")


def SEND_TEST(ALGORITHM_NAME, LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, BALANCE,
              TOTAL_COIN, TOTAL_INVESMENT, BUY_NUM, SELL_NUM, CLOSE_PRICE):
    BALANCE = round(BALANCE, 2)
    coinWallet = TOTAL_COIN * CLOSE_PRICE
    coinWallet = round(coinWallet, 2)
    TOTAL_COIN = round(TOTAL_COIN, 6)
    message = (f"Algorithm: {ALGORITHM_NAME}\n"
               f"Symbol: {LEFT_SMYBOL + RIGHT_SYMBOL} - Period: {CANDLE_PERIOD}\n"
               f"Total Transactions: {BUY_NUM + SELL_NUM}\n"
               f"Total Investment: {TOTAL_INVESMENT} - {RIGHT_SYMBOL}\n")
    if TOTAL_COIN != 0: message += (f"Total Coin: {TOTAL_COIN} - {LEFT_SMYBOL}\n"
                                    f"Current Wallet: {coinWallet} - {RIGHT_SYMBOL}")
    else: message += f"Current Wallet: {BALANCE} - {RIGHT_SYMBOL}"
    SEND(message)
# ----------------------------------------------------------------
