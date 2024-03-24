# ----------------------------------------------------------------
# Candle Default Settings
Candle_Limit = 1500
Candle_Periods = ["15m", "30m", "1h", "2h", "4h"]
# ----------------------------------------------------------------
# USDT Settings
Ignored_USDT_Balance = 5
MIN_USDT_Balance = 10
# ----------------------------------------------------------------
# Rate Settings
Binance_Comission_Rate = 0.99
Stop_Loss_Rate = 0.98
# ----------------------------------------------------------------
# Days Settings
Wallet_Change_Days = [1, 3, 7, 15, 30]
Coin_Change_Days = [7, 30, 90, 180, 365]
# ----------------------------------------------------------------
# Indicator Settings
MA_Lengths = [25, 50, 200]
RSI_Length = 15
StochRSI_Length = 5
StochRSI_Stoch_Length = 5
StochRSI_Smooth_K = 5
StochRSI_Smooth_D = 5
# ----------------------------------------------------------------
# Headers
Candle_Headers = ["Open Time", "Open Price", "High Price", "Low Price", "Close Price",
                  "Volume", "Close Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
Wallet_Headers = ["Coin", "Balance", "USDT Balance"]
Wallet_Changes_Headers = ["Total Balance", "1 Day Percent", "3 Day Percent", "7 Day Percent",
                          "15 Day Percent", "30 Day Percent", "AVG Percent"]
Coinlist_Changes_Headers = ["Coin", "7 Day Percent", "30 Day Percent", "90 Day Percent",
                            "180 Day Percent", "365 Day Percent", "AVG Percent"]
# ----------------------------------------------------------------
# Messages
Install_Message = ("Thank you for using Binance Efficient Yield Zonal Algorithm Bot!\nWe are currently making the "
                   "first installations. Please wait...")
Start_Message = ("I am Binance Efficient Yield Zonal Algorithm Bot. You can do Coin analysis, Coin backtest and "
                 "automatic buy and sell transactions with me.\nMore: '/info'")
Info_Message = ("Transactions:\n\nWrite Coinlist\nInsert Coinlist\nDrop Coinlist\nAnalysis Coinlist\n\nGet "
                "Wallet\nAnalysis Wallet\n\nAnalysis Coin\nBacktest Coin\n\nOpen Trade\nClose Trade\n\nMore: '/help'")
Help_Message = ("Tutorial:\n\nWrite Coinlist: It takes the coin symbols you have written below and creates a list of "
                "them.\nExample:\nMessage 1: 'Write Coinlist'\nMessage 2:\n          BTC\n          BNB\n          "
                "SOL\n          XEC\n          ...\n\nInsert Coinlist: You can see your Coin List and add "
                "to the list.\n\nDrop Coinlist: You can see your Coin List and delete it from the list.\n\nAnalysis "
                "Coinlist: It finds and sorts the min/max rising ones of the coin list you have already written and "
                "gives you a favorite/warning list. In order for this code to work, a Coin List must be "
                "written.\n\nGet Wallet: Lists all balances in your wallet.\n\nAnalysis Wallet: Allows you to view "
                "your wallet's changes from yesterday to today and your total/spot/earn balance.\n\nAnalysis Coin: It "
                "shares with you the indicator results and change percentage of the coin you typed.\n\nBacktest Coin: "
                "It shares with you all the buying and selling results of the coin you typed.\n\nOpen Trade: "
                "Initiates buy and sell transactions and buys at suitable opportunities.\n\nClose Trade: Performs "
                "sell transaction and transfers to cash\n\nMore: '/trade'")
Trade_Message = ("All rights of the code belong to Ilkay Beydah Saglam.\n\nThe code's sell strategy creates a new "
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
                 "progress of the extent of all the risk.")
# ----------------------------------------------------------------
