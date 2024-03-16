# ----------------------------------------------------------------
# Data Settings
CANDLE_LIMIT = 1500
CANDLE_PERIODS = ["30m", "1h", "2h", "4h", "8h"]
DATA_FOLDER_PATH = "../.data"
# ----------------------------------------------------------------
# Read Settings
CANDLE_HEADERS = ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
                  "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
WALLET_HEADERS = ["Coin", "Balance", "USDT_Balance"]
WALLET_CHANGES_HEADERS = ["Total_Balance", "1D_Percent", "3D_Percent", "7D_Percent",
                          "15D_Percent", "30D_Percent", "AVG_Percent"]
COINLIST_CHANGES_HEADERS = ["Coin_Symbol", "7D_Percent", "30D_Percent", "90D_Percent",
                            "180D_Percent", "365D_Percent", "AVG_Percent"]
# ----------------------------------------------------------------
# Write Settings
IGNORED_USDT_BALANCE = 1
WALLET_CHANGES_DAYS = [1, 3, 7, 15, 30]
COIN_CHANGES_DAYS = [7, 30, 90, 180, 365]
# ----------------------------------------------------------------
# Calculator Settings
STOP_LOSS_RATE = 0.98
BINANCE_COMISSION_RATE = 0.99
# ----------------------------------------------------------------
# Indicator Settings
MA_LENGTHS = [25, 50, 200]
RSI_LENGTH = 15
STOCHRSI_RSI_LENGTH = 5
STOCHRSI_STOCH_LENGTH = 5
STOCHRSI_SMOOTH_K = 5
STOCHRSI_SMOOTH_D = 5
# ----------------------------------------------------------------
# Trade Settings
TRADE_STOP = True
MIN_USDT_BALANCE = 5
# ----------------------------------------------------------------
# Bot Settings
# ----------------------------------------------------------------
# Message Settings
# ----------------------------------------------------------------
# Transactions Settings
START_MESSAGE = ("I am Binance Efficient Yield Zonal Algorithm Bot. You can do Coin analysis, Coin backtest and "
                 "automatic buy and sell transactions with me.\nMore: '/info'\n")
INFO_MESSAGE = ("Transactions:\n\nAnalysis Coin List\nWrite Coin List\nInsert Coin List\nDrop Coin List\n\nAnalysis "
                "Wallet\nGet Wallet\n\nAnalysis Coin\nBacktest Coin\n\nOpen Trade\nClose Trade\n\nMore: '/help'\n")
HELP_MESSAGE = ("Tutorial:\n\nAnalysis Coin List: It finds and sorts the min/max rising ones of the coin list you "
                "have already written and gives you a favorite/warning list. In order for this code to work, "
                "a Coin List must be written.\n\nWrite Coin List: It takes the coin symbols you have written below "
                "and creates a list of them.\nExample:\nMessage 1: 'Write Coin List'\nMessage 2:\n          BTC\n     "
                "     BNB\n          SOL\n          XEC\n          ...\n\nInsert Coin List: You can see your Coin "
                "List and add to the list.\n\nDrop Coin List: You can see your Coin List and delete it from the "
                "list.\n\n\nAnalysis Wallet: Allows you to view your wallet's changes from yesterday to today and "
                "your total/spot/earn balance.\n\nGet Wallet: Lists all balances in your wallet.\n\n\nAnalysis Coin: "
                "It shares with you the indicator results and change percentage of the coin you typed.\n\nBacktest "
                "Coin: It shares with you all the buying and selling results of the coin you typed.\n\n\nOpen Trade: "
                "Initiates buy and sell transactions and buys at suitable opportunities.\n\nClose Trade: Performs "
                "sell transaction and transfers to cash\n\n\nMore: '/trade'\n")
TRADE_MESSAGE = ("All rights of the code belong to Ilkay Beydah Saglam.\n\nThe code's sell strategy creates a new "
                 "sell signal by interpreting the satellite signals coming from EMA, SMA, Golden Cross, RSI, "
                 "StochRSI values and trades according to this signal. You can backtest some of your wealth symbols "
                 "before using this strategy.\n\nIf you want the code to buy and sell, you must go to the "
                 "src/settings/ parts in the application system and enter the Binance token and Binance confidential "
                 "information in the api.py data there. These values are provided by Binance and these values must "
                 "have Read permission and Spot / Margin sales permission.\n\nMany operations in the code are "
                 "performed or facilitated via telegram. To perform these operations, you must create a bot with Bot "
                 "Father on Telegram, go to the src/settings/ computer in the application system and paste the bot "
                 "token and your own User ID into the api.py data there.\n\nWhen you download and start using this "
                 "bot, you understand and approve all the risks and download it, and you are different from the "
                 "progress of the extent of all the risk.\n")
# ----------------------------------------------------------------
