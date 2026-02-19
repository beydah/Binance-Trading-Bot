
import pytest
import pandas as pd
from src.core import indicators as IND

# Sample data
@pytest.fixture
def sample_prices():
    # 200 data points usually needed for SMA200
    # Create a simple trend
    return pd.Series([i for i in range(250)])

def test_rsi_signal():
    # Oversold
    assert IND.F_Rsi_Signal(20) == 1
    # Overbought
    assert IND.F_Rsi_Signal(80) == -1
    # Neutral
    assert IND.F_Rsi_Signal(50) == 0

def test_dca_signal():
    # Price > SMA -> Buy/Up (1)
    assert IND.F_Dca_Signal(100, 110, 100, 105) == 1
    # Price < SMA -> Sell/Down (-1)
    # Wait, existing logic:
    # if p_prices > p_sma25: return 1
    # elif p_prices < p_sma25: return -1
    # It only compares current price to current sma
    assert IND.F_Dca_Signal(100, 90, 100, 100) == -1

def test_golden_cross_signal():
    # SMA50 > SMA200 -> 1 (Golden?)
    # Wait, usually Golden Cross is SMA50 crossing ABOVE SMA200.
    # Logic in code: if p_sma50 > p_sma200: return 1
    assert IND.F_Golden_Cross_Signal(50, 200, 50, 100) == 1
    assert IND.F_Golden_Cross_Signal(50, 50, 50, 100) == -1

def test_wrappers(sample_prices):
    # Just ensure they run without error and return expected shape
    # SMA 20
    sma20 = IND.F_Sma(20, sample_prices)
    assert len(sma20) == 250
    # First 19 should be NaN
    assert pd.isna(sma20[18])
    assert not pd.isna(sma20[19])

def test_golden_five(sample_prices):
    # Test the aggregate signal function
    # It calculates all indicators.
    # Since our sample data is a perfect uptrend:
    # Price > SMAs
    # SMA50 < SMA200 initially, then might cross?
    # 0..249. SMA50 at 200 will be (150+199)/2 = 174.5
    # SMA200 at 200 will be (0+199)/2 = 99.5
    # So SMA50 > SMA200 -> 1
    # Price (199) > SMA25 (187) -> 1
    # RSI on straight line? RSI of [0,1,2...] is 100 (after stabilization)
    # RSI 100 -> -1 (Overbought)
    
    # Let's just run it and ensure it returns [buy, sell] list
    signals = IND.F_Golden_Five(sample_prices)
    assert isinstance(signals, list)
    assert len(signals) == 2
    assert isinstance(signals[0], int)
    assert isinstance(signals[1], int)
