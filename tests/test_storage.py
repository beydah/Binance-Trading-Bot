
import pytest
import os
import shutil
from src.data import storage as STORE

@pytest.fixture
def temp_data_dir(tmp_path):
    # Setup: Override DATA_DIR in storage module
    original_dir = STORE.DATA_DIR
    STORE.DATA_DIR = str(tmp_path)
    
    yield tmp_path
    
    # Teardown
    STORE.DATA_DIR = original_dir

def test_save_load_coinlist(temp_data_dir):
    coins = ["BTC", "ETH", "BNB"]
    STORE.save_coinlist(coins)
    
    loaded = STORE.load_coinlist()
    assert loaded == coins
    
    # Test Append
    STORE.append_coinlist("SOL")
    loaded = STORE.load_coinlist()
    assert "SOL" in loaded
    assert len(loaded) == 4

def test_save_load_wallet(temp_data_dir):
    # Wallet is list of lists
    wallet = [
        ["BTC", 1.5, 75000.0],
        ["ETH", 10.0, 30000.0]
    ]
    STORE.save_wallet(wallet)
    
    loaded = STORE.load_wallet()
    # Loaded is DataFrame
    assert not loaded.empty
    assert len(loaded) == 2
    assert loaded.iloc[0]["Coin"] == "BTC"
    # CSV loads numbers as floats/ints
    assert float(loaded.iloc[0]["Balance"]) == 1.5

def test_save_load_candles(temp_data_dir):
    # [Open Time, Open, High, Low, Close, Vol, Close Time, ...]
    # Timestamps are ms ints
    candles = [
        [1600000000000, "100", "110", "90", "105", "1000", 1600000060000, 0, 0, 0, 0, 0]
    ]
    STORE.save_candles("BTC", "15m", candles)
    
    loaded = STORE.load_candles("BTC", "15m")
    assert not loaded.empty
    # Check if dates converted (storage.py converts 0 and 6 to datetime)
    import pandas as pd
    assert isinstance(loaded.iloc[0]["Open Time"], str) # Pandas reads as str/object usually unless parsed
    # Wait, storage.py converts to datetime object then writes csv. 
    # Validating existence and content is enough.
    assert float(loaded.iloc[0]["Open Price"]) == 100.0
