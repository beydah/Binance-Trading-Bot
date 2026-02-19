# ----------------------------------------------------------------
import time
import requests
from src.constants import TELEGRAM_TOKEN, TELEGRAM_USER_ID

def send_message(p_message: str):
    if not TELEGRAM_TOKEN or not TELEGRAM_USER_ID:
        print(f"Bot Message (No Token): {p_message}")
        return

    try:
        url = (f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
               f"/sendMessage?chat_id={TELEGRAM_USER_ID}"
               f"&parse_mode=Markdown&text={p_message}")
        requests.get(url)
    except Exception as e:
        print(f"Telegram Error: {e}")

def send_error(p_error: str):
    send_message(f"Error: {p_error}")
    # Original logic slept for 250s?
    time.sleep(10) # Reduced for sanity

def send_test_report(p_coin, p_period, p_first_date, p_last_date, p_buy_num, p_sell_num, p_entry_wallet,
                   p_monthly, p_total_inv, p_total_coin, p_price, p_wallet):
    message = (f"Symbol: {p_coin}USDT - Period: {p_period}\n\n"
               f"First Transaction Date: {p_first_date}\n"
               f"Last Transaction Date: {p_last_date}\n"
               f"Total Transactions: {p_buy_num+p_sell_num}\n\n"
               f"Entry Wallet: {p_entry_wallet} USDT\n"
               f"Monthly Addition: {p_monthly} USDT\n"
               f"Total Invesment: {p_total_inv} USDT\n\n")
    if p_total_coin > 0:
        message += (f"Total Coin: {round(p_total_coin, 4)} {p_coin}\n"
                    f"Current Wallet: {round(p_total_coin * p_price, 2)} USDT\n")
    else: message += f"Current Wallet: {round(p_wallet, 2)} USDT\n"
    
    send_message(message)
