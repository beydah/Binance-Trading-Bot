
import pytest
from src.core import calculations as CALC

def test_virtual_quantity():
    # Test valid quantity
    qty = CALC.F_Virtual_Quantity("Test", "BTC", 1.23456789, "0.00000100", "9000.00000000")
    assert qty == "1.234567"
    
    # Test min quantity limit
    qty = CALC.F_Virtual_Quantity("Test", "BTC", 0.0000001, "0.00000100", "9000.00000000")
    assert qty is None
    
    # Test max quantity limit
    qty = CALC.F_Virtual_Quantity("Test", "BTC", 10000.0, "0.00000100", "9000.00000000")
    assert qty.startswith("9000")

def test_find_coin_quantity():
    # 100 USDT / 50 Price = 2 Coin
    qty = CALC.F_Find_Coin_Quantity(100.0, 50.0)
    assert qty == 2.0
    
    # Precision check
    qty = CALC.F_Find_Coin_Quantity(10.0, 3.0)
    assert qty == 3.333333333

def test_find_usdt_quantity():
    # 2 Coin * 50 Price = 100 USDT
    val = CALC.F_Find_Usdt_Quantity(2.0, 50.0)
    assert val == 100.0

def test_find_wallet_change():
    # 100 to 110 = 10%
    change = CALC.F_Find_Wallet_Change(110.0, 100.0)
    assert change == 10.0
    
    # 100 to 90 = -10%
    change = CALC.F_Find_Wallet_Change(90.0, 100.0)
    assert change == -10.0
    
    # Zero division protection
    change = CALC.F_Find_Wallet_Change(100.0, 0.0)
    assert change == 0

def test_usdt_balance():
    # Above min balance (default 10)
    # 1 BTC * 50000 = 50000 > 10
    val = CALC.F_Usdt_Balance(1.0, 50000.0)
    assert val == 50000.0
    
    # Below min balance
    # 0.0001 BTC * 50000 = 5 < 10
    val = CALC.F_Usdt_Balance(0.0001, 50000.0)
    assert val == 0
