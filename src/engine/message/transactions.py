# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import bot as BOT
from src.engine.message import message as MESSAGE
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------
# Global Transaction Settings
MAIN_TRANSACTIONS = ["ANALYSIS_COIN_LIST", "WRITE_COIN_LIST", "INSERT_COIN_LIST", "DROP_COIN_LIST", "ANALYSIS_WALLET",
                     "GET_WALLET", "ANALYSIS_COIN", "BACKTEST_COIN", "OPEN_TRADE", "CLOSE_TRADE", "PROTOCOL"]
for i, TRANSACTION_NAME in enumerate(MAIN_TRANSACTIONS): globals()[TRANSACTION_NAME] = i
TRANSACTION_LOCK = [False] * len(MAIN_TRANSACTIONS)
TRANSACTION_LOCK[CLOSE_TRADE] = True
WRITE_TRANSACTION = [""]
WRITE_MODE = [False]
FIRST_TIME = [True]
# ----------------------------------------------------------------


def TRANSACTION(USERNAME, RAW_PROMPT, PROMPT):
    if not WRITE_MODE[0]:
        if PROMPT == "START": MESSAGE.SEND(f"Hello {USERNAME}! {DEF.START_MESSAGE}")
        elif PROMPT == "INFO": MESSAGE.SEND(DEF.INFO_MESSAGE)
        elif PROMPT == "HELP": MESSAGE.SEND(DEF.HELP_MESSAGE)
        elif PROMPT == "TRADE": MESSAGE.SEND(DEF.TRADE_MESSAGE)

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
                CALCULATE.WALLET_INFO()
                TRANSACTION_LOCK[ANALYSIS_WALLET] = False
            else: MESSAGE.SEND("Please wait...")
        elif PROMPT == "GET WALLET":
            if TRANSACTION_LOCK[GET_WALLET] is False:
                TRANSACTION_LOCK[GET_WALLET] = True
                DATA.GET_WALLET()
                TRANSACTION_LOCK[GET_WALLET] = False
            else: MESSAGE.SEND("Please wait...")
        elif PROMPT == "ANALYSIS COIN":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN FOR ANALYSIS"
            MESSAGE.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif PROMPT == "BACKTEST COIN":
            WRITE_MODE[0] = True
            WRITE_TRANSACTION[0] = "GET COIN FOR BACKTEST"
            MESSAGE.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif PROMPT == "OPEN TRADE" or PROMPT == "BEYZA START":
            if TRANSACTION_LOCK[OPEN_TRADE] is False:
                TRANSACTION_LOCK[OPEN_TRADE] = True
                TRANSACTION_LOCK[CLOSE_TRADE] = DEF.TRADE_STOP = False
                thread = LIB.THREAD.Thread(target=TRADE.BEYZA_START())
                thread.daemon = True
                thread.start()
            else: MESSAGE.SEND("The bot is already running...")
        elif PROMPT == "CLOSE TRADE" or PROMPT == "BEYZA STOP":
            if TRANSACTION_LOCK[CLOSE_TRADE] is False:
                TRANSACTION_LOCK[CLOSE_TRADE] = DEF.TRADE_STOP = True
                TRANSACTION_LOCK[OPEN_TRADE] = False
                TRADE.BEYZA_STOP()
            else: MESSAGE.SEND("The bot has already stopped...")

        elif PROMPT == "WHO IS YOUR CREATOR": MESSAGE.SEND("Ilkay Beydah Saglam")
        elif PROMPT == "WHO IS BEYZA": MESSAGE.SEND("Ilkay's Love")
        elif PROMPT == "WHO IS ILKAY": MESSAGE.SEND("Beyza's Love")
        elif PROMPT == "261021": MESSAGE.SEND("It's a beautiful day to love")
        elif PROMPT == "FIRST MOMENT": MESSAGE.SEND("If your bag was in your other hand, I would hold your hand")

        else: MESSAGE.SEND(f"{RAW_PROMPT} '/info'")
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
                CALCULATE.COIN_INFO(PROMPT)
                TRANSACTION_LOCK[ANALYSIS_COIN] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
        elif WRITE_TRANSACTION[0] == "GET COIN FOR BACKTEST":
            if not TRANSACTION_LOCK[BACKTEST_COIN]:
                TRANSACTION_LOCK[BACKTEST_COIN] = True
                TRADE.TEST(RAW_PROMPT)
                TRANSACTION_LOCK[BACKTEST_COIN] = False
                WRITE_MODE[0] = False
                WRITE_TRANSACTION[0] = ""
            else: MESSAGE.SEND("Please wait...")
    if FIRST_TIME[0]:
        FIRST_TIME[0] = False
        thread = LIB.THREAD.Thread(target=BOT.PROCESSOR())
        thread.daemon = True
        thread.start()

# ----------------------------------------------------------------
