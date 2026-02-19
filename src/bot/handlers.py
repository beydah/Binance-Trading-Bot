# ----------------------------------------------------------------
import threading
import time
from src.constants import START_MESSAGE, INFO_MESSAGE, HELP_MESSAGE, TRADE_MESSAGE, INSTALL_MESSAGE
from src.bot import messenger as MSG
from src.data import storage as STORE
from src.services import market_data_service as DATA
from src.core import calculations as CALC
from src.trading import strategy as STRATEGY

# State Management
class BotState:
    is_trading = False
    write_mode = None # "COINLIST", "INSERT", "DROP", "ANALYSIS", "BACKTEST"
    # Locks could be here but kept simple for now

# Global State Instance
STATE = BotState()

def _start_trading_loop():
    STATE.is_trading = True
    MSG.send_message("Trade Bot Started")
    
    while STATE.is_trading:
        # 1. Update Wallet & Sell
        # DATA.update_wallet() # Called inside strategy? No strategy calls update_wallet.
        # Strategy logic:
        # wallet = DATA.update_wallet()
        # STRATEGY.process_sell_signals(wallet)
        
        try:
            # We fetch wallet once and pass
            wallet = DATA.update_wallet()
            if wallet is not None:
                STRATEGY.process_sell_signals(wallet)
            
            # 2. Buy
            # Logic inside process_buy_signals handles fetching balance
            STRATEGY.process_buy_signals()
            
        except Exception as e:
             # Log error but don't crash
             print(f"Trade Loop Error: {e}")
             
        # Sleep
        time.sleep(5)
        
    MSG.send_message("Trade Bot Stopped")

def handle_message(user_name, raw_text):
    text = raw_text.upper().strip()
    
    # Check if we are in a Write Mode
    if STATE.write_mode:
        if text == "/EXIT" or text == "EXIT":
            STATE.write_mode = None
            MSG.send_message("Exited Write Mode")
            return

        if STATE.write_mode == "COINLIST":
            # Multi-line input? Original logic assumed single message with newlines
            # If text has newlines, split
            coins = [c.strip() for c in text.split('\n') if c.strip()]
            STORE.save_coinlist(coins)
            DATA.optimize_coinlist()
            MSG.send_message("Coinlist Saved")
            
        elif STATE.write_mode == "INSERT":
            # Single coin?
            DATA.store.append_coinlist(text)
            MSG.send_message(f"Inserted {text}")
            
        elif STATE.write_mode == "DROP":
            # Load, remove, save
            current = STORE.load_coinlist()
            if text in current:
                current.remove(text)
                STORE.save_coinlist(current)
                MSG.send_message(f"Dropped {text}")
            else:
                MSG.send_message(f"{text} not found")

        elif STATE.write_mode == "BACKTEST":
            # Format: Coin, Entry, Monthly
            parts = [p.strip() for p in text.split(',')]
            coin = parts[0]
            entry = float(parts[1]) if len(parts) > 1 else 1000
            monthly = float(parts[2]) if len(parts) > 2 else 100
            
            # Run backtest
            MSG.send_message(f"Running Backtest for {coin}...")
            # STRATEGY.backtest(coin, entry, monthly) # Need to implement backtest wrapper
            
        STATE.write_mode = None
        return

    # Normal Commands
    if text == "START": MSG.send_message(f"Hello {user_name}! {START_MESSAGE}")
    elif text == "INFO": MSG.send_message(INFO_MESSAGE)
    elif text == "HELP": MSG.send_message(HELP_MESSAGE)
    elif text == "TRADE": MSG.send_message(TRADE_MESSAGE)
    
    # Write Commands
    elif text == "WRITE COINLIST":
        STATE.write_mode = "COINLIST"
        MSG.send_message("Enter Coinlist (one per line). Type '/exit' to cancel.")
        
    elif text == "INSERT COINLIST":
        STATE.write_mode = "INSERT"
        MSG.send_message("Enter Coin to Insert. Type '/exit' to cancel.")
        
    elif text == "DROP COINLIST":
        STATE.write_mode = "DROP"
        MSG.send_message("Enter Coin to Drop. Type '/exit' to cancel.")
        
    # Analysis
    elif text == "ANALYSIS WALLET":
        DATA.calculate_wallet_changes() # Updates CSV
        # Send info? 
        # Original: CALCULATE.F_Wallet_Changes_Info() -> Sends Msg
        # We need a function to format and send
        MSG.send_message("Wallet Analysis Updated (Check CSV or Implement Display)")

    elif text == "OPEN TRADE":
        if not STATE.is_trading:
            t = threading.Thread(target=_start_trading_loop)
            t.daemon = True
            t.start()
        else:
            MSG.send_message("Trade is already running")
            
    elif text == "CLOSE TRADE":
        if STATE.is_trading:
            STATE.is_trading = False # Loop will stop
        else:
            MSG.send_message("Trade is not running")
            
    # Etc... (Easter eggs removed for brevity but can extend)
    else:
        MSG.send_message(f"Unknown command: {text}. Try '/info'")
