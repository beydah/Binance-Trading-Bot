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
from src.engine.message import message as MSG
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------
# Global Transaction Settings
Main_Transactions = ["ANALYSIS_COIN_LIST", "WRITE_COIN_LIST", "INSERT_COIN_LIST", "DROP_COIN_LIST", "ANALYSIS_WALLET",
                     "GET_WALLET", "ANALYSIS_COIN", "BACKTEST_COIN", "OPEN_TRADE", "CLOSE_TRADE", "PROTOCOL"]
for i, Transaction_Name in enumerate(Main_Transactions): globals()[Transaction_Name] = i
Transaction_Lock = [False] * len(Main_Transactions)
Write_Mode = [False]
Write_Transaction = [""]
Trade_Stop = Transaction_Lock[CLOSE_TRADE] = [True]
# ----------------------------------------------------------------


def TRANSACTION(User_Name, Raw_Prompt, Prompt):
    if not Write_Mode[0]:
        if Prompt == "START": MSG.SEND(f"Hello {User_Name}! {DEF.Start_Message}")
        elif Prompt == "INFO": MSG.SEND(DEF.Info_Message)
        elif Prompt == "HELP": MSG.SEND(DEF.Help_Message)
        elif Prompt == "TRADE": MSG.SEND(DEF.Trade_Message)

        elif Prompt == "ANALYSIS COIN LIST":
            if Transaction_Lock[ANALYSIS_COIN_LIST] is False:
                MSG.SEND("I Analyses...")
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = True
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = True
                DATA.GET_COINLIST_INFO()
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = False
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = False
            else: MSG.SEND("Please Wait...")
        elif Prompt == "WRITE COIN LIST":
            Write_Mode[0] = True
            Write_Transaction[0] = "GET COIN LIST FOR WRITE"
            MSG.SEND("Enter the coin list. But becareful:\n(To Exit: '/exit')")
        elif Prompt == "INSERT COIN LIST":
            Write_Mode[0] = True
            Write_Transaction[0] = "GET COIN FOR INSERT"
            MSG.SEND(f"Coin List:\n{READ.COINLIST()}\n")
            MSG.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif Prompt == "DROP COIN LIST":
            Write_Mode[0] = True
            Write_Transaction[0] = "GET COIN FOR DROP"
            MSG.SEND(f"Coin List:\n{READ.COINLIST()}\n")
            MSG.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif Prompt == "ANALYSIS WALLET":
            if Transaction_Lock[ANALYSIS_WALLET] is False:
                MSG.SEND("I Analyses...")
                Transaction_Lock[ANALYSIS_WALLET] = True
                CALCULATE.WALLET_INFO()
                Transaction_Lock[ANALYSIS_WALLET] = False
            else: MSG.SEND("Please Wait...")
        elif Prompt == "GET WALLET":
            if Transaction_Lock[GET_WALLET] is False:
                Transaction_Lock[GET_WALLET] = True
                DATA.GET_WALLET()
                Transaction_Lock[GET_WALLET] = False
            else: MSG.SEND("Please Wait...")
        elif Prompt == "ANALYSIS COIN":
            Write_Mode[0] = True
            Write_Transaction[0] = "GET COIN FOR ANALYSIS"
            MSG.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
        elif Prompt == "BACKTEST COIN":
            Write_Mode[0] = True
            Write_Transaction[0] = "GET COIN FOR BACKTEST"
            MSG.SEND("Enter the coin. But becareful:\nFormule: Coin,Entry USDT,Monthly USDT\n(To Exit: '/exit')")
        elif Prompt == "OPEN TRADE" or Prompt == "BEYZA START":
            if Transaction_Lock[OPEN_TRADE] is False:
                Transaction_Lock[OPEN_TRADE] = True
                Transaction_Lock[CLOSE_TRADE] = Trade_Stop[0] = False
                thread = LIB.THREAD(target=TRADE.BEYZA_START)
                thread.start()
            else: MSG.SEND("Bot is Already Running.")
        elif Prompt == "CLOSE TRADE" or Prompt == "BEYZA STOP":
            if Transaction_Lock[CLOSE_TRADE] is False:
                Transaction_Lock[CLOSE_TRADE] = Trade_Stop[0] = True
                Transaction_Lock[OPEN_TRADE] = False
                TRADE.BEYZA_STOP()
            else: MSG.SEND("Bot has Already Stopped.")

        elif Prompt == "WHO IS YOUR CREATOR": MSG.SEND("Ilkay Beydah Saglam")
        elif Prompt == "WHO IS BEYZA": MSG.SEND("Ilkay's Love")
        elif Prompt == "WHO IS ILKAY": MSG.SEND("Beyza's Love")
        elif Prompt == "261021": MSG.SEND("It's a beautiful day to love")
        elif Prompt == "FIRST MOMENT": MSG.SEND("If your bag was in your other hand, I would hold your hand")

        else: MSG.SEND(f"{Raw_Prompt} '/info'")
    elif Write_Mode[0]:
        if Prompt == "EXIT":
            MSG.SEND("I am Exit.")
            Write_Mode[0] = False
            Write_Transaction[0] = ""

        elif Write_Transaction[0] == "GET COIN LIST FOR WRITE":
            if not Transaction_Lock[WRITE_COIN_LIST]:
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = True
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = True
                WRITE.COINLIST(Prompt)
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = False
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = False
                Write_Mode[0] = False
                Write_Transaction[0] = ""
            else: MSG.SEND("Please Wait...")
        elif Write_Transaction[0] == "GET COIN FOR INSERT":
            if not Transaction_Lock[WRITE_COIN_LIST]:
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = True
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = True
                WRITE.INSERT_COINLIST(Prompt)
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = False
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = False
                Write_Mode[0] = False
                Write_Transaction[0] = ""
            else: MSG.SEND("Please Wait...")
        elif Write_Transaction[0] == "GET COIN FOR DROP":
            if not Transaction_Lock[WRITE_COIN_LIST]:
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = True
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = True
                WRITE.DROP_COINLIST(Prompt)
                Transaction_Lock[ANALYSIS_COIN_LIST] = Transaction_Lock[WRITE_COIN_LIST] = False
                Transaction_Lock[INSERT_COIN_LIST] = Transaction_Lock[DROP_COIN_LIST] = False
                Write_Mode[0] = False
                Write_Transaction[0] = ""
            else: MSG.SEND("Please Wait...")
        elif Write_Transaction[0] == "GET COIN FOR ANALYSIS":
            if not Transaction_Lock[ANALYSIS_COIN]:
                Transaction_Lock[ANALYSIS_COIN] = True
                CALCULATE.COIN_INFO(Prompt)
                Transaction_Lock[ANALYSIS_COIN] = False
                Write_Mode[0] = False
                Write_Transaction[0] = ""
            else: MSG.SEND("Please Wait...")
        elif Write_Transaction[0] == "GET COIN FOR BACKTEST":
            if not Transaction_Lock[BACKTEST_COIN]:
                Transaction_Lock[BACKTEST_COIN] = True
                TRADE.TEST(Raw_Prompt)
                Transaction_Lock[BACKTEST_COIN] = False
                Write_Mode[0] = False
                Write_Transaction[0] = ""
            else: MSG.SEND("Please Wait...")
# ----------------------------------------------------------------
