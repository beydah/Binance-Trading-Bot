# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import wallet as WALLET

from src.engine import algorithm as ALGORITHM
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL
from src.engine import analysis as ANALYSIS

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------
# Global Transaction Settings
TRANSACTIONS = ["ANALYSIS_COIN_LIST", "ANALYSIS_WALLET", "WRITE_COIN_LIST",
                "ANALYSIS_COIN", "BACKTEST_COIN", "OPEN_TRADE", "CLOSE_TRADE"]
for i, TRANSACTION_NAME in enumerate(TRANSACTIONS): globals()[TRANSACTION_NAME] = i
TRANSACTION_LOCK = [False, False, False, False, False, False, False]
WRITE_TRANSACTION = [""]
WRITE_MODE = [False]
# ----------------------------------------------------------------


# Get Operations
def START():
    bot = LIB.BOT(API.TELEGRAM_BOT_TOKEN)
    bot.set_update_listener(GET)
    while True:
        try:
            bot.polling()
            break
        except Exception as e:
            print(f"Error: {e}")
            LIB.SLEEP(15)


def GET(messages):
    for message in messages:
        if str(message.from_user.id) == API.TELEGRAM_USER_ID:
            if not WRITE_MODE[0]:
                if message.text.upper() == "/START": SEND(f"Hello {message.from_user.first_name}! I am Binance "
                                                          f"Trading Bot. You can do Coin analysis, Coin backtest and "
                                                          f"automatic buy and sell transactions with me. For more "
                                                          f"information type '/info'")
                elif message.text.upper() == "/INFO": SEND("**Creating a Coin List:**\n* `Write Coin List`\n* Write "
                                                           "at least 10 coins under each other.\n* Example:\n     "
                                                           "Message 1: Write Coin List\n     Message 2: \n      BTC\n "
                                                           "     ETH\n      BNB\n      SOL\n      XRP\n      "
                                                           "...\n\n**Coin List Analysis:**\n* `Analysis Coin List`\n* "
                                                           "See the highest/lowest risers.\n\n**Coin Analysis:**\n* "
                                                           "`Analysis Coin`\n* Analyze a coin (risky as I can't "
                                                           "follow the news).\n* Example:\n     Message 1: Analysis "
                                                           "Coin\n     Message 2: BTC\n\n**Backtest:**\n* `Backtest "
                                                           "Coin`\n* See the results of buy/sell algorithms before "
                                                           "buying a coin.\n* Example:\n     Message 1: Backtest "
                                                           "Coin\nMessage 2: BTC\n\n**Wallet Analysis:**\n* `Analysis "
                                                           "Wallet`\n* Analyze your spot and otherassets in your "
                                                           "Binance wallet.\n* Binance API integration "
                                                           "required.\n\n**Automatic Buy/Sell Transactions:**\n* "
                                                           "`Open Trade`\n* Coin List and Binance API integration "
                                                           "required.\n* Buy/sell signals are based on indicators and "
                                                           "do not follow the news.\n* Warning: All risks are at your "
                                                           "own risk.\n\n**Closing All Transactions:**\n* `Close "
                                                           "Trade`\n* Trading mode turned on and Binance API "
                                                           "integration required.\n")
                elif message.text.upper() == "ANALYSIS COIN LIST":
                    if TRANSACTION_LOCK[ANALYSIS_COIN_LIST] is False:
                        SEND("I analyses...")
                        TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = True
                        TRANSACTION_LOCK[WRITE_COIN_LIST] = True
                        ANALYSIS.COINLIST_INFO()
                        TRANSACTION_LOCK[WRITE_COIN_LIST] = False
                        TRANSACTION_LOCK[ANALYSIS_COIN_LIST] = False
                    else: SEND("Please wait...")
                elif message.text.upper() == "ANALYSIS WALLET":
                    if TRANSACTION_LOCK[ANALYSIS_WALLET] is False:
                        SEND("I analyses...")
                        TRANSACTION_LOCK[ANALYSIS_WALLET] = True
                        ANALYSIS.WALLET_INFO()
                        TRANSACTION_LOCK[ANALYSIS_WALLET] = False
                    else: SEND("Please wait...")
                elif message.text.upper() == "WRITE COIN LIST":
                    WRITE_MODE[0] = True
                    WRITE_TRANSACTION[0] = "GET COIN LIST"
                    SEND("Enter the coin list. But becareful:\n(To Exit: /exit)")
                elif message.text.upper() == "ANALYSIS COIN":
                    WRITE_MODE[0] = True
                    WRITE_TRANSACTION[0] = "GET COIN FOR ANALYSIS"
                    SEND("Enter the coin. But becareful:\n(To Exit: /exit)")
                elif message.text.upper() == "BACKTEST COIN":
                    WRITE_MODE[0] = True
                    WRITE_TRANSACTION[0] = "GET COIN FOR BACKTEST"
                    SEND("Enter the coin. But becareful:\n(To Exit: /exit)")
                elif message.text.upper() == "OPEN TRADE": pass  # TODO: TRADE.OPEN()
                elif message.text.upper() == "CLOSE TRADE": pass  # TODO: TRADE.CLOSE()
                elif message.text.upper() == "WHO IS YOUR CREATOR": SEND("Ilkay Beydah Saglam")
                elif message.text.upper() == "261021": SEND("It's A Lovely Day")
                elif message.text.upper() == "BEYZA": SEND("Ilkay's Love")
                else: SEND(f"{message.text} /info")
            elif WRITE_MODE[0]:
                if message.text.upper() == "/EXIT":
                    SEND("Ok.")
                    WRITE_MODE[0] = False
                    WRITE_TRANSACTION[0] = ""
                elif WRITE_TRANSACTION[0] == "GET COIN LIST":
                    if not TRANSACTION_LOCK[WRITE_COIN_LIST]:
                        TRANSACTION_LOCK[WRITE_COIN_LIST] = True
                        LIST.WRITE_COIN(message.text.upper())
                        TRANSACTION_LOCK[WRITE_COIN_LIST] = False
                        SEND("Ok.")
                        WRITE_MODE[0] = False
                        WRITE_TRANSACTION[0] = ""
                    else: SEND("Please wait...")
                elif WRITE_TRANSACTION[0] == "GET COIN FOR ANALYSIS":
                    if not TRANSACTION_LOCK[ANALYSIS_COIN]:
                        TRANSACTION_LOCK[ANALYSIS_COIN] = True
                        ANALYSIS.COIN_INFO(message.text.upper())
                        TRANSACTION_LOCK[ANALYSIS_COIN] = False
                        WRITE_MODE[0] = False
                        WRITE_TRANSACTION[0] = ""
                    else: SEND("Please wait...")
                elif WRITE_TRANSACTION[0] == "GET COIN FOR BACKTEST":
                    if not TRANSACTION_LOCK[BACKTEST_COIN]:
                        TRANSACTION_LOCK[BACKTEST_COIN] = True
                        ALGORITHM.FULLTEST(message.text.upper())
                        TRANSACTION_LOCK[BACKTEST_COIN] = False
                        WRITE_MODE[0] = False
                        WRITE_TRANSACTION[0] = ""
                    else: SEND("Please wait...")
        else: return
# ----------------------------------------------------------------


# Send Operations
def SEND(BOT_MESSAGE):
    print(BOT_MESSAGE)
    try: LIB.REQUEST.get(f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
                         f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
                         f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    except Exception as e: print(f"Error: {e}")


def SEND_TEST(ALGORITHM_NAME, LEFT_SMYBOL, RIGHT_SYMBOL, CANDLE_PERIOD, BALANCE,
              TOTAL_COIN, TOTAL_INVESMENT, BUY_NUM, SELL_NUM, CLOSE_PRICE):
    BALANCE = round(BALANCE, 2)
    coinWallet = round((TOTAL_COIN * CLOSE_PRICE), 2)
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
