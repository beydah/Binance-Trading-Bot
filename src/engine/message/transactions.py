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
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# THREAD
from src.engine.thread import timer as TIMER
from src.engine.thread import debugger as DEBUGGER
from src.engine.thread import processor as PROCESSOR
# ----------------------------------------------------------------
# Global Transaction Settings
MAIN_TRANSACTIONS = ["ANALYSIS_COIN_LIST", "WRITE_COIN_LIST", "INSERT_COIN_LIST", "DROP_COIN_LIST", "ANALYSIS_WALLET",
                     "GET_WALLET", "ANALYSIS_COIN", "BACKTEST_COIN", "OPEN_TRADE", "CLOSE_TRADE"]
for i, TRANSACTION_NAME in enumerate(MAIN_TRANSACTIONS): globals()[TRANSACTION_NAME] = i
TRANSACTION_LOCK = [False] * len(MAIN_TRANSACTIONS)
WRITE_TRANSACTION = [""]
WRITE_MODE = [False]
# ----------------------------------------------------------------


def TRANSACTION(USERNAME, PROMPT):
    if not WRITE_MODE[0]:
        if PROMPT == "START":
            MESSAGE.SEND(f"Hello {USERNAME}! I am Binance Efficient Yield Zonal Algorithm Bot. You can do Coin "
                         f"analysis, Coin backtest and automatic buy and sell transactions with me.\nMore: '/info'\n")
        elif PROMPT == "INFO":
            MESSAGE.SEND("Transactions:\n\nAnalysis Coin List\nWrite Coin List\nInsert Coin List\nDrop Coin "
                         "List\n\nAnalysis Wallet\nGet Wallet\n\nAnalysis Coin\nBacktest Coin\n\nOpen Trade\nClose "
                         "Trade\n\nMore: '/help'\n")
        elif PROMPT == "HELP":
            MESSAGE.SEND("Tutorial:\n\nAnalysis Coin List: It finds and sorts the min/max rising ones of the coin "
                         "list you have already written and gives you a favorite/warning list. In order for this code "
                         "to work, a Coin List must be written.\n\nWrite Coin List: It takes the coin symbols you "
                         "have written below and creates a list of them.\nExample:\nMessage 1: 'Write Coin "
                         "List'\nMessage 2:\n          BTC\n          BNB\n          SOL\n          XEC\n          "
                         "...\n\nInsert Coin List: You can see your Coin List and add to the list.\n\nDrop Coin List: "
                         "You can see your Coin List and delete it from the list.\n\n\nAnalysis Wallet: Allows you to "
                         "view your wallet's changes from yesterday to today and your total/spot/earn balance.\n\nGet "
                         "Wallet: Lists all balances in your wallet.\n\n\nAnalysis Coin: It shares with you the "
                         "indicator results and change percentage of the coin you typed.\n\nBacktest Coin: It shares "
                         "with you all the buying and selling results of the coin you typed.\n\n\nOpen Trade: "
                         "Initiates buy and sell transactions and buys at suitable opportunities.\n\nClose Trade: "
                         "Performs sell transaction and transfers to cash\n\n\nMore: '/trade'\n")
        elif PROMPT == "TRADE":
            MESSAGE.SEND("All rights of the code belong to Ilkay Beydah Saglam.\n\nThe code's sell strategy creates a "
                         "new sell signal by interpreting the satellite signals coming from EMA, SMA, Golden Cross, "
                         "RSI, StochRSI values and trades according to this signal. You can backtest some of your "
                         "wealth symbols before using this strategy.\n\nIf you want the code to buy and sell, "
                         "you must go to the src/settings/ parts in the application system and enter the Binance "
                         "token and Binance confidential information in the api.py data there. These values are "
                         "provided by Binance and these values must have Read permission and Spot / Margin sales "
                         "permission.\n\nMany operations in the code are performed or facilitated via telegram. To "
                         "perform these operations, you must create a bot with Bot Father on Telegram, "
                         "go to the src/settings/ computer in the application system and paste the bot token and your "
                         "own User ID into the api.py data there.\n\nWhen you download and start using this bot, "
                         "you understand and approve all the risks and download it, and you are different from the "
                         "progress of the extent of all the risk.\n")

        elif PROMPT == "ANALYSIS COIN LIST":
            if TRANSACTION_LOCK[ANALYSIS_COIN_LIST] is False:
                MESSAGE.SEND("I analyses...")
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = True
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = True
                DATA.GET_COINLIST_INFO()
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = False
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = False
            else: MESSAGE.SEND("Please wait...")
        elif PROMPT == "WRITE COIN LIST":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN LIST FOR WRITE"
            MESSAGE.SEND("Enter the coin list. But becareful:\n(To Exit: '/exit')")
        elif PROMPT == "INSERT COIN LIST":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN FOR INSERT"
            MESSAGE.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif PROMPT == "DROP COIN LIST":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN FOR DROP"
            MESSAGE.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif PROMPT == "ANALYSIS WALLET":
            if TRANSACTION_LOCK[ANALYSIS_WALLET] is False:
                MESSAGE.SEND("I analyses...")
                TRANSACTION_LOCK[ANALYSIS_WALLET] = True
                DATA.GET_WALLET_INFO()
                TRANSACTION_LOCK[ANALYSIS_WALLET] = False
            else: MESSAGE.SEND("Please wait...")
        elif PROMPT == "GET WALLET":
            if TRANSACTION_LOCK[GET_WALLET] is False:
                TRANSACTION_LOCK[GET_WALLET] = True
                MESSAGE.SEND(DATA.GET_WALLET())
                TRANSACTION_LOCK[GET_WALLET] = False
            else: MESSAGE.SEND("Please wait...")
        elif PROMPT == "ANALYSIS COIN":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN FOR ANALYSIS"
            MESSAGE.SEND("Enter the coin. But becareful:\n(To Exit: /exit)")
        elif PROMPT == "BACKTEST COIN":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN FOR BACKTEST"
            MESSAGE.SEND("Enter the coin. But becareful:\n(To Exit: /exit)")
        elif PROMPT == "OPEN TRADE": pass  # TODO: TRADE.OPEN()
        elif PROMPT == "CLOSE TRADE": pass  # TODO: TRADE.CLOSE()

        elif PROMPT == "WHO IS YOUR CREATOR": MESSAGE.SEND("Ilkay Beydah Saglam")
        elif PROMPT == "WHO IS BEYZA": MESSAGE.SEND("Ilkay's Love")
        elif PROMPT == "WHO IS ILKAY": MESSAGE.SEND("Beyza's Love")
        elif PROMPT == "261021": MESSAGE.SEND("Sevmek icin guzel bir gun")
        elif PROMPT == "FIRST MOMENT": MESSAGE.SEND("Cantan diger elinde olsaydi elini tutardim")

        else: MESSAGE.SEND(f"{PROMPT} /info")
    elif WRITE_MODE[0]:
        if PROMPT == "EXIT":
            MESSAGE.SEND("I am exit.")
            WRITE_MODE[0] = False
            WRITE_TRANSACTION[0] = ""

        elif WRITE_TRANSACTION[0] == "GET COIN LIST FOR WRITE":
            if not TRANSACTION_LOCK[WRITE_COIN_LIST]:
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = True
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = True
                WRITE.COINLIST(PROMPT)
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = False
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
        elif WRITE_TRANSACTION[0] == "GET COIN FOR INSERT":
            if not TRANSACTION_LOCK[WRITE_COIN_LIST]:
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = True
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = True
                WRITE.INSERT_COINLIST(PROMPT)
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = False
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
        elif WRITE_TRANSACTION[0] == "GET COIN FOR DROP":
            if not TRANSACTION_LOCK[WRITE_COIN_LIST]:
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = True
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = True
                WRITE.DROP_COINLIST(PROMPT)
                TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = TRANSACTION_LOCK[WRITE_COIN_LIST] = False
                TRANSACTION_LOCK[INSERT_COIN_LIST] = TRANSACTION_LOCK[DROP_COIN_LIST] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
        elif WRITE_TRANSACTION[0] == "GET COIN FOR ANALYSIS":
            if not TRANSACTION_LOCK[ANALYSIS_COIN]:
                TRANSACTION_LOCK[ANALYSIS_COIN] = True
                DATA.GET_COIN_INFO(PROMPT)
                TRANSACTION_LOCK[ANALYSIS_COIN] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
        elif WRITE_TRANSACTION[0] == "GET COIN FOR BACKTEST":
            if not TRANSACTION_LOCK[BACKTEST_COIN]:
                TRANSACTION_LOCK[BACKTEST_COIN] = True
                TRADE.TEST(PROMPT)
                TRANSACTION_LOCK[BACKTEST_COIN] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
# ----------------------------------------------------------------
