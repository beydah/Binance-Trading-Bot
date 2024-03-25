# ----------------------------------------------------------------
# Added Links
# MESSAGE
from src.engine.bot import transactions as T
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
# ----------------------------------------------------------------


def GET(Messages):
    for message in Messages:
        if str(message.from_user.id) == API.Telegram_User_ID:
            print(f"{message.from_user.first_name}:\n{message.text}\n")
            prompt = ""
            for char in message.text.upper():
                if char not in LIB.STRING.punctuation: prompt += char
            T.TRANSACTION(message.from_user.first_name, message.text.upper(), prompt)
# ----------------------------------------------------------------


def SEND(Bot_Message):
    print(f"Bot:\n{Bot_Message}\n")
    try:
        LIB.REQUEST.get(f"https://api.telegram.org/bot{API.Telegram_Bot_Token}"
                        f"/sendMessage?chat_id={API.Telegram_User_ID}"
                        f"&parse_mode=Markdown&text={Bot_Message}")
    except Exception: pass


def SEND_TEST(Coin, Period, First_Transaction_Date, Last_Transaction_Date, Buy_Num, Sell_Num, Entry_Wallet,
              Monthly_Addition, Total_Invesment, Total_Coin, Price, Wallet):
    message = (f"Symbol: {Coin}USDT - Period: {Period}\n\n"
               f"First Transaction Date: {First_Transaction_Date}\n"
               f"Last Transaction Date: {Last_Transaction_Date}\n"
               f"Total Transactions: {Buy_Num+Sell_Num}\n\n"
               f"Entry Wallet: {Entry_Wallet} USDT\n"
               f"Monthly Addition: {Monthly_Addition} USDT\n"
               f"Total Invesment: {Total_Invesment} USDT\n\n")
    if Total_Coin > 0:
        message += (f"Total Coin: {round(Total_Coin, 4)} {Coin}\n"
                    f"Current Wallet: {round(Total_Coin * Price, 2)} USDT\n")
    else: message += f"Current Wallet: {round(Wallet, 2)} USDT\n"
    SEND(message)


def SEND_ERROR(Error):
    SEND(f"Error {Error}")
    LIB.TIME.sleep(15)
# ----------------------------------------------------------------
