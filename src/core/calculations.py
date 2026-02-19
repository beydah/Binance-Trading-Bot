# ----------------------------------------------------------------
from decimal import Decimal
from src.constants import MIN_USDT_BALANCE
from src.utils.logger import LOGGER

def F_Virtual_Quantity(p_transaction: str, p_coin: str, p_quantity: float, p_min_qty: str, p_max_qty: str):
    """
    Calculates the correct quantity based on Binance limits.
    """
    try:
        if Decimal(p_min_qty) > p_quantity:
            LOGGER.warning(f"Quantity Error: Min {float(p_min_qty)} > Request {float(p_quantity)}")
            return None
        
        if Decimal(p_max_qty) < p_quantity: p_quantity = Decimal(p_max_qty)
        
        min_step = 0
        for char in p_min_qty:
            if char == "0": min_step += 1
            elif char == "1": break
            
        if p_quantity == int(p_quantity): virtual_quantity = f"{int(p_quantity)}."+("0" * 8)
        else: virtual_quantity = str(Decimal(p_quantity))
        
        left_str, right_str = virtual_quantity.split(".")
        right_str = right_str[:min_step]
        
        if right_str == "": return left_str
        return f"{left_str}.{right_str}"
    except Exception as e:
        LOGGER.error(f"Error in F_Virtual_Quantity: {e}")
        return None

def F_Find_Coin_Quantity(p_usdt_quantity: float, p_coin_price: float): 
    return float(round(p_usdt_quantity / p_coin_price, 9))

def F_Find_Usdt_Quantity(p_coin_quantity: float, p_coin_price: float): 
    return float(round(p_coin_quantity * p_coin_price, 9))

def F_Find_Wallet_Change(p_now_balance: float, p_past_balance: float):
    try: 
        if p_past_balance == 0: return 0
        return round((p_now_balance - p_past_balance) / p_past_balance * 100, 2)
    except Exception: return 0

def F_Usdt_Balance(p_balance: float, p_coin_price: float):
    """
    Calculates USDT equivalent of a coin balance using provided price.
    """
    usdt_balance = F_Find_Usdt_Quantity(p_coin_quantity=p_balance, p_coin_price=p_coin_price)
    if usdt_balance > MIN_USDT_BALANCE: return float(round(usdt_balance, 3))
    return 0
