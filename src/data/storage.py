# ----------------------------------------------------------------
import os
import csv
import pandas as pd
from src.constants import CANDLE_HEADERS, WALLET_HEADERS, WALLET_CHANGES_HEADERS, COINLIST_CHANGES_HEADERS, DATA_DIR
from src.utils.logger import LOGGER

# Ensure Data Directory Exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def _get_path(p_filename: str):
    return os.path.join(DATA_DIR, p_filename)

# region Generic CSV I/O
def save_csv(p_filename: str, p_data: list, p_mode: str = 'w'):
    try:
        path = _get_path(p_filename)
        with open(path, p_mode, newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(p_data)
        return path
    except Exception as e:
        LOGGER.error(f"Error saving CSV {p_filename}: {e}")
        return None

def load_csv(p_filename: str, p_headers: list = None):
    try:
        path = _get_path(p_filename)
        if not os.path.exists(path): return None
        if p_headers:
            return pd.read_csv(path, names=p_headers)
        return pd.read_csv(path)
    except Exception as e:
        LOGGER.error(f"Error loading CSV {p_filename}: {e}")
        return None
# endregion

# region Specific Data Storage
def save_candles(p_coin: str, p_period: str, p_candles: list):
    filename = f"{p_coin}_{p_period}.csv"
    # Format dates (index 0 and 6)
    # Note: Logic moved here from write.py
    from datetime import datetime
    for candle in p_candles:
        candle[0] = datetime.fromtimestamp(candle[0] / 1000)
        candle[6] = datetime.fromtimestamp(candle[6] / 1000)
    
    return save_csv(filename, p_candles)

def load_candles(p_coin: str, p_period: str):
    filename = f"{p_coin}_{p_period}.csv"
    path = _get_path(filename)
    if not os.path.exists(path): return None
    # We load with headers
    return load_csv(filename, CANDLE_HEADERS)

def delete_candle_file(p_coin: str, p_period: str):
    filename = f"{p_coin}_{p_period}.csv"
    path = _get_path(filename)
    if os.path.exists(path):
        os.remove(path)

def save_wallet(p_data: list):
    # p_data is list of lists
    return save_csv("wallet.csv", p_data)

def load_wallet():
    return load_csv("wallet.csv", WALLET_HEADERS)

def save_coinlist(p_coins: list):
    try:
        path = _get_path("coinlist.txt")
        with open(path, 'w', newline='') as file:
            for coin in p_coins:
                file.write(f"{coin}\n")
    except Exception as e:
        LOGGER.error(f"Error saving coinlist: {e}")

def load_coinlist():
    try:
        path = _get_path("coinlist.txt")
        if not os.path.exists(path): return []
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        LOGGER.error(f"Error loading coinlist: {e}")
        return []

def append_coinlist(p_coin: str):
    try:
        path = _get_path("coinlist.txt")
        with open(path, 'a', newline='') as file:
            file.write(f"{p_coin}\n")
    except Exception as e:
        LOGGER.error(f"Error appending coinlist: {e}")

def save_wallet_changes(p_row: list, p_mode='a'):
    # Check if file needs headers or exists? Original didn't use headers in file, just data
    # Logic: if file doesn't exist, create empty?
    # We just append the row
    return save_csv("wallet_changes.csv", [p_row], p_mode)

def load_wallet_changes():
    return load_csv("wallet_changes.csv", WALLET_CHANGES_HEADERS)

def save_coinlist_changes(p_data: list):
    return save_csv("coinlist_changes.csv", p_data)

def load_coinlist_changes():
    return load_csv("coinlist_changes.csv", COINLIST_CHANGES_HEADERS)

def save_favoritelist(p_coins: list):
    # List of single item lists
    return save_csv("favoritelist.csv", [[c] for c in p_coins])

def load_favoritelist():
    df = load_csv("favoritelist.csv", [WALLET_HEADERS[0]]) # "Coin"
    return df
# endregion
