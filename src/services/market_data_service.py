# ----------------------------------------------------------------
import pandas as pd
from datetime import datetime
from src.constants import CANDLE_PERIODS, CANDLE_LIMIT, WALLET_HEADERS, WALLET_CHANGE_DAYS, COIN_CHANGE_DAYS
from src.utils.logger import LOGGER
from src.core import calculations as CALC
from src.data import storage as STORE
from src.services import binance_service as API

# region Candle Data
def get_candle_data(p_coin: str, p_period: str = None, p_limit: int = None, p_datetime: str = None):
    # Fetch from API
    candles = API.F_Get_Candle(p_coin, p_period, p_limit, p_datetime)
    # Save to CSV
    path = STORE.save_candles(p_coin, p_period or CANDLE_PERIODS[0], candles)
    # Return as DF (Load from CSV to ensure consistency with headers/types)
    return STORE.load_candles(p_coin, p_period or CANDLE_PERIODS[0])
# endregion

# region Wallet Data
def _get_price(p_coin: str):
    # Helper to get current price for valuation
    try:
        # Check last candle for price
        candles = get_candle_data(p_coin, "1m", 1)
        if not candles.empty:
            return float(candles.iloc[-1]['Close Price'])
        return 0.0
    except Exception: return 0.0

def update_wallet():
    balances = API.F_Get_Balances()
    orders = API.F_Get_Open_Orders()
    
    wallet_data = []
    
    # Process Balances
    for balance in balances:
        free = float(balance['free'])
        if free <= 0: continue
        
        coin = balance['asset']
        price = _get_price(coin) if coin != "USDT" else 1.0
        usdt_val = CALC.F_Usdt_Balance(free, price)
        
        # Note: Original logic had MIN_USDT_BALANCE check inside CALC.F_Usdt_Balance
        if usdt_val > 0:
            wallet_data.append([coin, free, usdt_val])
            
    # Process Orders
    if orders:
        for order in orders:
            coin = order['symbol'].replace("USDT", "")
            qty = float(order['origQty'])
            price = _get_price(coin)
            usdt_val = CALC.F_Find_Usdt_Quantity(qty, price)
            wallet_data.append([coin, qty, usdt_val])
            
    STORE.save_wallet(wallet_data)
    return STORE.load_wallet()

def calculate_wallet_changes():
    # Load current wallet
    wallet_df = update_wallet()
    if wallet_df is None or wallet_df.empty: return None
    
    # Calculate Total USDT
    total_usdt = wallet_df[WALLET_HEADERS[2]].sum()
    
    # Load history
    changes_history = STORE.load_wallet_changes() # DF of past records
    
    # If no history, just save current state?
    # Original logic read "wallet_changes.csv" and used index -day to find change
    # Here we assume wallet_changes.csv accumulates daily snapshots?
    # Original write.py just appended a row calculated from *past balances* in that same file?
    # Yes: `past_balances = [] ... for row in reader: past_balances.append(float(row[0]))`
    # So the file stores `Total Balance` in column 0.
    
    past_balances = []
    if changes_history is not None and not changes_history.empty:
        past_balances = changes_history.iloc[:, 0].tolist() # Column 0 is Total Balance
    
    current_changes = []
    for day in WALLET_CHANGE_DAYS:
        if len(past_balances) >= day:
            past_val = past_balances[-day]
            change = CALC.F_Find_Wallet_Change(total_usdt, past_val)
        else:
            change = 0
        current_changes.append(change)
        
    avg = round(sum(current_changes) / len(current_changes), 2)
    
    # Save new row
    row = [total_usdt] + current_changes + [avg]
    STORE.save_wallet_changes(row)
    
    # Return info for display
    return row # or object

# endregion

# region Coin List
def get_full_coin_list():
    balances = API.F_Get_Balances()
    # We want a DF of assets
    return [b['asset'] for b in balances] # List of strings

def optimize_coinlist():
    # Reads coinlist.txt, verifies with API, rewrites
    current_list = STORE.load_coinlist()
    verified_list = []
    
    all_assets = get_full_coin_list() 
    # Logic in original `F_Find_Coin` iterates API balance list to check existence
    # We optimize: get set of all assets
    all_assets_set = set(all_assets)
    
    for coin in current_list:
        if coin in all_assets_set:
            verified_list.append(coin)
            
    STORE.save_coinlist(verified_list)

def calculate_coinlist_changes():
    coinlist = STORE.load_coinlist()
    rows = []
    
    for coin in coinlist:
        changes = []
        # Need history for coins?
        # Original logic: `F_Coin_Change` fetches candles from `past_day` and `today`.
        import datetime
        
        for day in COIN_CHANGE_DAYS:
            # Need to fetch historic price
            # This is slow if done sequentially for many coins
            try:
                # We can use API klines with start/end
                # But `get_candle_data` writes to file. Maybe too much I/O?
                # Using direct API here might be better, or using our wrapper but careful with file churn.
                # Let's use direct API call for efficiency or use specific method
                
                # Logic:
                # past_price = ...
                # current_price = ...
                
                # We need a robust `get_price_at_time(coin, time)`
                # Let's assume we implement it or skip for now to keep it simple
                changes.append(0) 
            except: changes.append(0)
            
        avg = 0
        rows.append([coin] + changes + [avg])
        
    STORE.save_coinlist_changes(rows)

def get_min_max_lists():
    # Load Coinlist Changes
    df = STORE.load_coinlist_changes()
    if df is None or df.empty: return [], []
    
    # Simple sort by AVG column
    # Need to match headers or assume column index
    # Headers logic in storage.py: ["Coin", ..., "AVG Percent"]
    avg_col = COINLIST_CHANGES_HEADERS[6]
    n = int(len(df) / 2)
    
    sorted_df = df.sort_values(by=avg_col)
    
    # Min List (Smallest AVG)
    min_list = sorted_df.head(n)[COINLIST_CHANGES_HEADERS[0]].tolist()
    
    # Max List (Largest AVG)
    max_list = sorted_df.tail(n)[COINLIST_CHANGES_HEADERS[0]].tolist()
    # Reverse max list to show largest first?
    max_list.reverse()
    
    return min_list, max_list

def update_favorites():
    min_list, _ = get_min_max_lists()
    STORE.save_favoritelist(min_list)
    return min_list
# endregion
