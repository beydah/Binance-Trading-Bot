# ----------------------------------------------------------------
from src.utils.logger import LOGGER
from src.constants import STOP_LOSS_RATE, BINANCE_COMISSION_RATE
from src.core import calculations as CALC
from src.services import binance_service as API
from src.services import market_data_service as DATA

# Helper to check quantity (Calls symbol info -> API)
def _get_qty_limits(p_coin: str):
    min_qty = API.F_Get_Symbol_Info(p_coin, "minQty")
    max_qty = API.F_Get_Symbol_Info(p_coin, "maxQty")
    return min_qty, max_qty

def execute_market_buy(p_coin: str, p_quantity: float):
    min_qty, max_qty = _get_qty_limits(p_coin)
    virtual_qty = CALC.F_Virtual_Quantity("Market Buy", p_coin, p_quantity, min_qty, max_qty)
    
    if virtual_qty is None: return False
    
    try:
        client = API.F_Get_Binance()
        client.order_market(symbol=p_coin+"USDT", side="BUY", quantity=virtual_qty)
        LOGGER.info(f"MARKET BUY executed: {virtual_qty} {p_coin}")
        # Send message? Ideally return True and let caller send message
        return True
    except Exception as e:
        LOGGER.error(f"MARKET BUY failed: {e}")
        return False

def execute_market_sell(p_coin: str, p_quantity: float):
    min_qty, max_qty = _get_qty_limits(p_coin)
    virtual_qty = CALC.F_Virtual_Quantity("Market Sell", p_coin, p_quantity, min_qty, max_qty)
    
    if virtual_qty is None: return False
    
    try:
        client = API.F_Get_Binance()
        client.order_market(symbol=p_coin+"USDT", side="SELL", quantity=virtual_qty)
        LOGGER.info(f"MARKET SELL executed: {virtual_qty} {p_coin}")
        return True
    except Exception as e:
        LOGGER.error(f"MARKET SELL failed: {e}")
        return False

def place_stop_loss(p_coin: str):
    # Determine quantity from wallet
    # This requires reading wallet balance for the coin
    # In original logic: READ.F_Wallet(p_coin, 1) -> Balance
    try:
        wallet = DATA.update_wallet() # Or load? update is safer but slower
        # Find coin balance
        balance = 0
        min_qty, max_qty = _get_qty_limits(p_coin)
        
        # Need to implement finding balance from wallet data
        # Assuming wallet is list of [Coin, Free, USDT]
        for row in wallet: # row is list
             if row[0] == p_coin:
                 balance = float(row[1])
                 break
        
        if balance == 0: return False

        virtual_qty = CALC.F_Virtual_Quantity("Stop Loss", p_coin, balance, min_qty, max_qty)
        if virtual_qty is None: return False

        # Get Current Price
        price = DATA.get_candle_data(p_coin, "1m", 1).iloc[-1]['Close Price']
        stop_price = CALC.F_Find_Usdt_Quantity(float(price), STOP_LOSS_RATE) # Reuse calc or just math? 
        # Original: round(float(price[0]) * DEF.STOP_LOSS_RATE, len(str(price[0]).split(".")[-1]))
        stop_price = round(float(price) * STOP_LOSS_RATE, 2) # Simplify rounding for now or use precise logic
        
        client = API.F_Get_Binance()
        client.create_order(symbol=p_coin+"USDT", type="STOP_LOSS_LIMIT", side="SELL",
                            price=str(stop_price), stopPrice=str(stop_price), 
                            quantity=virtual_qty, timeInForce="GTC")
        LOGGER.info(f"STOP LOSS placed for {p_coin} at {stop_price}")
        return True
    except Exception as e:
        LOGGER.error(f"STOP LOSS failed: {e}")
        return False

def remove_stop_loss(p_coin: str):
    try:
        order = API.F_Get_Stop_Loss_Order(p_coin)
        if order:
            client = API.F_Get_Binance()
            client.cancel_order(symbol=p_coin+"USDT", orderId=order['orderId'])
            LOGGER.info(f"STOP LOSS removed for {p_coin}")
            return True
        return False
    except Exception as e:
        LOGGER.error(f"REMOVE STOP LOSS failed: {e}")
        return False
