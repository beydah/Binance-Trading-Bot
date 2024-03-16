# ----------------------------------------------------------------
# Added Links
# MESSAGE
from src.engine.message import bot as BOT
from src.engine.message import transactions as T
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
# ----------------------------------------------------------------


def GET(messages):
    for message in messages:
        if str(message.from_user.id) == API.TELEGRAM_USER_ID:
            print(f"{message.from_user.first_name}:\n{message.text}\n")
            prompt = ""
            for char in message.text.upper():
                if char not in LIB.STRING.punctuation: prompt += char
            T.TRANSACTION(message.from_user.first_name, message.text.upper(), prompt)
# ----------------------------------------------------------------


def SEND(BOT_MESSAGE):
    print(f"Bot:\n{BOT_MESSAGE}\n")
    try:
        LIB.REQUEST.get(f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
                        f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
                        f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    except Exception as e: print(f"Error Message Send: {e}")


def SEND_TEST(COIN, CANDLE_PERIOD, FIRST_TRANSACTION_DATE, LAST_TRANSACTION_DATE, BUY_NUM, SELL_NUM, ENTRY_WALLET,
              MONTHLY_ADDITION, TOTAL_INVESMENT, TOTAL_COIN, CLOSE_PRICE, WALLET):
    message = (f"Symbol: {COIN}USDT - Period: {CANDLE_PERIOD}\n\n"
               f"First Transaction Date: {FIRST_TRANSACTION_DATE}\n"
               f"Last Transaction Date: {LAST_TRANSACTION_DATE}\n"
               f"Total Transactions: {BUY_NUM + SELL_NUM}\n\n"
               f"Entry Wallet: {ENTRY_WALLET} USDT\n"
               f"Monthly Addition: {MONTHLY_ADDITION} USDT\n"
               f"Total Invesment: {TOTAL_INVESMENT} USDT\n\n")
    if TOTAL_COIN > 0:
        message += (f"Total Coin: {round(TOTAL_COIN, 4)} {COIN}\n"
                    f"Current Wallet: {round((round(TOTAL_COIN, 4) * CLOSE_PRICE), 2)} USDT\n")
    else: message += f"Current Wallet: {round(WALLET, 2)} USDT\n"
    SEND(message)


def SEND_ERROR(ERROR):
    SEND(f"Error {ERROR}")
    LIB.TIME.sleep(15)
# ----------------------------------------------------------------
