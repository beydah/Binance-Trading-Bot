# ----------------------------------------------------------------
import time
from src.utils.logger import LOGGER
from src.constants import MIN_USDT_BALANCE, CANDLE_PERIODS, STOP_LOSS_RATE, WALLET_HEADERS
from src.core import indicators as IND
from src.services import market_data_service as DATA
from src.services import trading_service as EXECUTE
from src.core import calculations as CALC

# Trading State Flags (Shared state? Or passed?)
# Original code used global T.Transaction.
# We should use a State Manager or simplistic global state in specific module.
# Let's assume bot/main.py manages high level state flags if possible, or we keep a state module.
# For now, we will perform pure logic checks here or assume caller manages locks.

def check_stop_loss(p_coin: str, p_price: float, p_stop_loss_price: float):
    try:
        current_price = float(p_price)
        stop_price = float(p_stop_loss_price)
        
        # Trailing Stop Loss Logic (Move up if price increases significantly?)
        # Original: if (price * 0.98) > stop_loss_price: Move Up
        if (current_price * STOP_LOSS_RATE) > stop_price:
            LOGGER.info(f"Updating Stop Loss for {p_coin}")
            EXECUTE.remove_stop_loss(p_coin)
            EXECUTE.place_stop_loss(p_coin) # Places new SL based on current price
            return False
            
        elif current_price < stop_price:
            LOGGER.info(f"Stop Loss Triggered for {p_coin}")
            # Order is already filled by Binance if STOP_LOSS_LIMIT.
            # But original code had logic to "Delete and Market Sell"? 
            # Or reliance on Binance order?
            # Original code: binance.create_order(... STOP_LOSS_LIMIT ...)
            # Then check_stop_loss: if price < stop: Delete SL (why?), return True (Sold?)
            # If Binance triggers it, order is filled. We just need to cleanup or update internal state.
            EXECUTE.remove_stop_loss(p_coin)
            return True
            
        return False
    except Exception as e:
        LOGGER.error(f"Error checking SL {p_coin}: {e}")
        return False

def process_sell_signals(p_wallet_df):
    for index, row in p_wallet_df.iterrows():
        # index is 0..N, row is series.
        # Assuming headers: Coin, Balance, USDT
        coin = row[WALLET_HEADERS[0]]
        qty = row[WALLET_HEADERS[1]]
        usd_val = row[WALLET_HEADERS[2]]
        
        if coin.startswith("LD") or coin == "USDT": continue
        if usd_val <= MIN_USDT_BALANCE: continue
        
        LOGGER.info(f"Checking Sell Signal for {coin}...")
        
        # 1. Stop Loss Check
        # Need current price
        candles = DATA.get_candle_data(p_coin=coin, p_period="1m", p_limit=1)
        if candles.empty: continue
        current_price = float(candles.iloc[-1]['Close Price'])
        
        # Get SL Order
        # We need a way to get existing SL price.
        # EXECUTE service / API service needed
        import src.services.binance_service as API
        sl_order = API.F_Get_Stop_Loss_Order(coin)
        
        sl_price = current_price * 0.95 # Default loose SL if none exists?
        if sl_order: sl_price = float(sl_order['stopPrice'])
        
        if check_stop_loss(coin, current_price, sl_price):
             # If SL triggered manually or we want to force close?
             # If SL triggered by price < stop, Binance executes it. 
             # We might just be detecting it happened.
             continue

        # 2. Indicator Check
        # Load long period candles
        long_candles = DATA.get_candle_data(coin, CANDLE_PERIODS[4], 205) # 4h
        if len(long_candles) < 205: continue
        
        prices = long_candles['Close Price'].astype(float).tolist()
        gf = IND.F_Golden_Five(prices)
        if IND.F_Golden_Five_Signal(gf) == 1: continue # Strong Buy -> Hold
        
        # Confirmation
        short_candles = DATA.get_candle_data(coin, CANDLE_PERIODS[0], 205) # 15m? Or defaults?
        prices_s = short_candles['Close Price'].astype(float).tolist()
        if IND.F_Golden_Five_Signal(IND.F_Golden_Five(prices_s)) != -1: continue # Not sell
        
        # Sell
        LOGGER.info(f"Sell Signal Confirmed: {coin}")
        EXECUTE.remove_stop_loss(coin)
        EXECUTE.execute_market_sell(coin, qty)

def process_buy_signals():
    # Load favorites
    try:
        favorites = DATA.STORE.load_favoritelist() # Direct storage access or via service with `load_favorites`
        if favorites is None or favorites.empty: return
        
        # Check USDT
        wallet = DATA.update_wallet()
        # Find USDT
        usdt_row = wallet[wallet[WALLET_HEADERS[0]] == "USDT"]
        if usdt_row.empty: return
        usdt_balance = float(usdt_row.iloc[0][WALLET_HEADERS[1]])
        
        invest_amount = usdt_amount = usdt_balance / 2
        if invest_amount <= MIN_USDT_BALANCE: return
        
        for index, row in favorites.iterrows():
            coin = row[WALLET_HEADERS[0]] # Coin
            
            # Indicators
            long_candles = DATA.get_candle_data(coin, CANDLE_PERIODS[4], 205)
            if len(long_candles) < 205: continue
            
            prices = long_candles['Close Price'].astype(float).tolist()
            if IND.F_Golden_Five_Signal(IND.F_Golden_Five(prices)) == -1: continue # Sell signal
            
            # Confirmation
            short_candles = DATA.get_candle_data(coin, CANDLE_PERIODS[0], 205)
            prices_s = short_candles['Close Price'].astype(float).tolist()
            if IND.F_Golden_Five_Signal(IND.F_Golden_Five(prices_s)) != 1: continue # Not buy
            
            # Exec
            LOGGER.info(f"Buy Signal Confirmed: {coin}")
            # Calculate quantity
            current_candles = DATA.get_candle_data(coin, "1m", 1)
            price = float(current_candles.iloc[-1]['Close Price'])
            qty = CALC.F_Find_Coin_Quantity(usdt_amount, price)
            
            result = EXECUTE.execute_market_buy(coin, qty)
            if result:
                EXECUTE.remove_stop_loss(coin)
                EXECUTE.place_stop_loss(coin)
                
    except Exception as e:
        LOGGER.error(f"Process Buy Signals Error: {e}")

def backtest(p_coin: str, p_period: str, p_wallet_u: float, p_monthly: float):
    # Logic from trade.py F_Backtest
    # Need to return results string or print it
    # Implementation similiar to original using IND functions
    pass 
