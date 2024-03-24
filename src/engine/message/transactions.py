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
from src.engine.message import message as MSG
# SETTING
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------
Main_Transactions = ["Coinlist", "Wallet", "Coin", "Trade", "Write"]
for i, Transaction_Name in enumerate(Main_Transactions): globals()[Transaction_Name] = i
Transaction = [False] * len(Main_Transactions)
Write_Transaction = [""]
# ----------------------------------------------------------------


def TRANSACTION(User_Name, Raw_Prompt, Prompt):
    if not Transaction[Write]:
        # ----------------------------------------------------------------
        if Prompt == "START": MSG.SEND(f"Hello {User_Name}! {DEF.Start_Message}")
        elif Prompt == "INFO": MSG.SEND(DEF.Info_Message)
        elif Prompt == "HELP": MSG.SEND(DEF.Help_Message)
        elif Prompt == "TRADE": MSG.SEND(DEF.Trade_Message)
        # ----------------------------------------------------------------
        elif Prompt == "WRITE COINLIST":
            if not Transaction[Coinlist]:
                Transaction[Write] = True
                Write_Transaction[0] = "GET COINLIST FOR WRITE"
                MSG.SEND("Enter the coinlist. But becareful:\n(To Exit: '/exit')")
            else: MSG.SEND("Please Wait...")
        elif Prompt == "INSERT COINLIST":
            if not Transaction[Coinlist]:
                Transaction[Write] = True
                Write_Transaction[0] = "GET COIN FOR INSERT"
                MSG.SEND(f"Coin List:\n{READ.COINLIST()}\nEnter the coin. But becareful:\n(To Exit: '/exit')")
            else: MSG.SEND("Please Wait...")
        elif Prompt == "DROP COINLIST":
            if not Transaction[Coinlist]:
                Transaction[Write] = True
                Write_Transaction[0] = "GET COIN FOR DROP"
                MSG.SEND(f"Coin List:\n{READ.COINLIST()}\nEnter the coin. But becareful:\n(To Exit: '/exit')")
            else: MSG.SEND("Please Wait...")
        elif Prompt == "ANALYSIS COINLIST":
            if not Transaction[Coinlist]:
                MSG.SEND("I Analyses...")
                DATA.GET_COINLIST_INFO()
            else: MSG.SEND("Please Wait...")
        # ----------------------------------------------------------------
        elif Prompt == "GET WALLET":
            if not Transaction[Wallet]: DATA.GET_WALLET_INFO()
            else: MSG.SEND("Please Wait...")
        elif Prompt == "ANALYSIS WALLET":
            if not Transaction[Wallet]:
                MSG.SEND("I Analyses...")
                CALCULATE.WALLET_CHANGES_INFO()
            else: MSG.SEND("Please Wait...")
        # ----------------------------------------------------------------
        elif Prompt == "ANALYSIS COIN":
            if not Transaction[Coin]:
                Transaction[Write] = True
                Write_Transaction[0] = "GET COIN FOR ANALYSIS"
                MSG.SEND("Enter the coin. But becareful:\n(To Exit: '/exit')")
            else: MSG.SEND("Please Wait...")
        elif Prompt == "BACKTEST COIN":
            if not Transaction[Coin]:
                Transaction[Write] = True
                Write_Transaction[0] = "GET COIN FOR BACKTEST"
                MSG.SEND("Enter the coin. But becareful:\nFormule: Coin, Entry USDT, Monthly USDT\n(To Exit: '/exit')")
            else: MSG.SEND("Please Wait...")
        # ----------------------------------------------------------------
        elif Prompt == "OPEN TRADE" or Prompt == "BEYZA START":
            if not Transaction[Trade]:
                thread = LIB.THREAD(target=TRADE.BEYZA_START)
                thread.start()
            else: MSG.SEND("Bot is Already Running")
        elif Prompt == "CLOSE TRADE" or Prompt == "BEYZA STOP":
            if Transaction[Trade]: TRADE.BEYZA_STOP()
            else: MSG.SEND("Bot has Already Stopped")
        # ----------------------------------------------------------------
        elif Prompt == "WHO IS YOUR CREATOR": MSG.SEND("Ilkay Beydah Saglam")
        elif Prompt == "WHO IS ILKAY": MSG.SEND("Beyza's Love")
        elif Prompt == "WHO IS BEYZA": MSG.SEND("Ilkay's Love")
        elif Prompt == "261021": MSG.SEND("It's a beautiful day to love")
        elif Prompt == "FIRST MOMENT": MSG.SEND("If your bag was in your other hand, I would hold your hand")
        else: MSG.SEND(f"{Raw_Prompt} '/info'")
    else:
        if Prompt == "EXIT": MSG.SEND("I am Exit")
        # ----------------------------------------------------------------
        elif Write_Transaction[0] == "GET COINLIST FOR WRITE": WRITE.COINLIST(Prompt)
        elif Write_Transaction[0] == "GET COIN FOR INSERT": WRITE.INSERT_COINLIST(Prompt)
        elif Write_Transaction[0] == "GET COIN FOR DROP": WRITE.DROP_COINLIST(Prompt)
        elif Write_Transaction[0] == "GET COIN FOR ANALYSIS": CALCULATE.COIN_INFO(Prompt)
        elif Write_Transaction[0] == "GET COIN FOR BACKTEST": TRADE.TEST(Raw_Prompt)
        # ----------------------------------------------------------------
        Transaction[Write] = False
        Write_Transaction[0] = ""
# ----------------------------------------------------------------
