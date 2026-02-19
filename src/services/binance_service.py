# ----------------------------------------------------------------
import os
import time
from binance.client import Client
from dotenv import load_dotenv
from src.utils.logger import LOGGER
from src.constants import CANDLE_PERIODS, CANDLE_LIMIT

# Note: Messenger import delayed to avoid circular dependency if possible, 
# or we will import inside functions if necessary.
# For now, we will handle errors by logging and potentially re-raising or using a local error handler.
# To maintain original behavior (sending Telegram msg on error), we might need to import messenger.
# However, messenger depends on transactions which depends on... 
# Let's import messenger inside methods if needed or use a robust logger.

# Load environment variables
load_dotenv()

# API Keys
BINANCE_KEY = os.getenv("BINANCE_KEY", "")
BINANCE_SECRET = os.getenv("BINANCE_SECRET", "")

# Client Initialization
if BINANCE_KEY and BINANCE_SECRET:
    BINANCE = Client(BINANCE_KEY, BINANCE_SECRET)
else:
    BINANCE = None
    LOGGER.warning("Binance API Keys not found. Client not initialized.")

def _send_error(p_error: str):
    # Local helper to avoid circular import issues at top level
    try:
        from src.bot.messenger import F_Send_Error
        F_Send_Error(p_error)
    except ImportError:
        LOGGER.error(f"Could not send error to Telegram: {p_error}")

def F_Get_Binance():
    # In original checks if None and tries to re-init? No, just returns global.
    # Original logic: while True try return API.Binance except error MSG.
    return BINANCE

def F_Get_Server_Time():
    client = F_Get_Binance()
    while True:
        try: return client.get_server_time()["serverTime"]
        except Exception as e: 
            LOGGER.error(f"GET_BINANCE_SERVER_TIME: {e}")
            _send_error(f"GET_BINANCE_SERVER_TIME: {e}")
            time.sleep(5) # Add delay to prevent spam loop

def F_Get_Candle(p_coin: str, p_period: str = None, p_limit: int = None, p_datetime: str = None):
    client = F_Get_Binance()
    if p_period is None: p_period = CANDLE_PERIODS[0]
    if p_limit is None: p_limit = CANDLE_LIMIT
    while True:
        try: return client.get_historical_klines(symbol=p_coin+"USDT", interval=p_period, end_str=p_datetime, limit=p_limit)
        except Exception as e: 
            LOGGER.error(f"GET_CANDLE: {e}")
            _send_error(f"GET_CANDLE: {e}")
            time.sleep(5)

def F_Get_Symbol_Info(p_coin: str, p_info: str):
    client = F_Get_Binance()
    while True:
        try: return client.get_symbol_info(p_coin+"USDT")['filters'][1][p_info]
        except Exception as e: 
            LOGGER.error(f"GET_SYMBOLINFO: {e}")
            _send_error(f"GET_SYMBOLINFO: {e}")
            time.sleep(5)

def F_Get_Last_Price(p_coin: str):
    client = F_Get_Binance()
    while True:
        try: return client.get_my_trades(symbol=p_coin+"USDT", limit=1)[0]['price']
        except Exception as e: 
            LOGGER.error(f"GET_LAST_PRICE: {e}")
            _send_error(f"GET_LAST_PRICE: {e}")
            time.sleep(5)

# Utility for Time Gap (from data.py)
def F_Find_Time_Gap(p_time_gap: int, p_error: str):
    if p_time_gap < 10000: return p_time_gap + 1000
    else:
        _send_error(p_error)
        return 0

def F_Get_Open_Orders(p_symbol: str = None):
    client = F_Get_Binance()
    time_gap = 0
    while True:
        try: return client.get_open_orders(symbol=p_symbol, timestamp=F_Get_Server_Time() - time_gap)
        except Exception as e: 
            LOGGER.error(f"GET_OPEN_ORDERS: {e}")
            time_gap = F_Find_Time_Gap(p_time_gap=time_gap, p_error=f"GET_OPEN_ORDERS: {e}")
            time.sleep(1)

def F_Get_Stop_Loss_Order(p_coin: str):
    while True:
        try:
            open_orders = F_Get_Open_Orders(p_coin+"USDT")
            if open_orders is None: return None
            for order in open_orders:
                if order['type'] == 'STOP_LOSS_LIMIT' and order['side'] == 'SELL': return order
            return None
        except Exception as e: 
            LOGGER.error(f"DELETE_STOP_LOSS: {e}")
            _send_error(f"DELETE_STOP_LOSS: {e}")
            time.sleep(5)

def F_Get_Account():
    client = F_Get_Binance()
    time_gap = 0
    while True:
        try: return client.get_account(timestamp=F_Get_Server_Time() - time_gap)
        except Exception as e: 
            LOGGER.error(f"GET_ACCOUNT: {e}")
            time_gap = F_Find_Time_Gap(p_time_gap=time_gap, p_error=f"GET_ACCOUNT: {e}")
            time.sleep(1)

def F_Get_Balances(): return F_Get_Account()['balances']
