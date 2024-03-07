# ----------------------------------------------------------------
# Added Links
# DATA
import string

from src.engine.data import data as DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import indicator as INDICATOR
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import bot as BOT
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


def GET(messages):
    for message in messages:
        if str(message.from_user.id) == API.TELEGRAM_USER_ID:
            print(f"{message.from_user.first_name}:\n{message.text}\n")
            prompt = ""
            for char in message.text.upper():
                if char not in string.punctuation: prompt += char
            TRANSACTIONS.TRANSACTION(message.from_user.first_name, prompt)
# ----------------------------------------------------------------


def SEND(BOT_MESSAGE):
    print(f"Bot:\n{BOT_MESSAGE}\n")
    try: LIB.REQUEST.get(f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
                         f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
                         f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    except Exception: print(f"Error Message Send: {Exception}")


def SEND_TEST(COIN, CANDLE_PERIOD, WALLET, TOTAL_COIN, TOTAL_INVESMENT, BUY_NUM, SELL_NUM, CLOSE_PRICE):
    message = (f"Symbol: {COIN}USDT - Period: {CANDLE_PERIOD}\n"
               f"Total Transactions: {BUY_NUM + SELL_NUM}\n"
               f"Total Investment: {TOTAL_INVESMENT} - USDT\n")
    if round(TOTAL_COIN, 4) > 0:
        message += (f"Total Coin: {round(TOTAL_COIN, 4)} - {COIN}\n"
                    f"Current Wallet: {round((round(TOTAL_COIN, 4) * CLOSE_PRICE), 2)} - USDT")
    else: message += f"Current Wallet: {round(WALLET, 2)} - USDT"
    SEND(message)


def SEND_ERROR(ERROR):
    SEND(f"Error {ERROR}")
    LIB.TIME.sleep(15)
# ----------------------------------------------------------------
