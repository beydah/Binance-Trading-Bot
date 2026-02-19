
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from src.services import market_data_service as M_DATA
from src.services import trading_service as TRADE

# region Market Data Service Tests
@patch('src.services.market_data_service.API')
@patch('src.services.market_data_service.STORE')
def test_get_candle_data(mock_store, mock_api):
    # Setup
    mock_api.F_Get_Candle.return_value = []
    # Mock return from loading
    mock_store.load_candles.return_value = pd.DataFrame({'Close Price': [100.0]})
    
    # Run
    df = M_DATA.get_candle_data("BTC")
    
    # Verify
    mock_api.F_Get_Candle.assert_called_once()
    mock_store.save_candles.assert_called_once()
    assert not df.empty
    assert df.iloc[0]['Close Price'] == 100.0

@patch('src.services.market_data_service.API')
@patch('src.services.market_data_service.STORE')
def test_update_wallet(mock_store, mock_api):
    # Mock API Balances
    mock_api.F_Get_Balances.return_value = [
        {'asset': 'BTC', 'free': '1.0'},
        {'asset': 'USDT', 'free': '100.0'}
    ]
    mock_api.F_Get_Open_Orders.return_value = []
    
    # Mock Price Fetch (get_candle_data used internally)
    # We need to mock get_candle_data inside market_data_service?
    # Or just mock API call since get_candle_data calls API.
    # But get_candle_data also calls STORE.
    # It's easier if we mock API.F_Get_Candle to return data that allows price extraction.
    
    # However, update_wallet calls local _get_price which calls get_candle_data.
    # If we mocked API.F_Get_Candle in setup, it works.
    
    # Mock STORE load to return what we saved
    mock_store.load_wallet.return_value = pd.DataFrame([
        {'Coin': 'BTC', 'Balance': 1.0, 'USDT Balance': 50000.0}
    ])
    
    # execution
    # We need to simulate price fetch. _get_price -> get_candle_data -> API.F_Get_Candle
    # API.F_Get_Candle returns list of lists.
    # We need to return a structure that becomes a DF with 'Close Price'
    # Actually, get_candle_data returns result of STORE.load_candles.
    # So we must mock STORE.load_candles to return a DF with 'Close Price'.
    
    mock_store.load_candles.return_value = pd.DataFrame({'Close Price': [50000.0]})
    
    result = M_DATA.update_wallet()
    
    mock_store.save_wallet.assert_called_once()
    assert not result.empty

# endregion

# region Trading Service Tests
@patch('src.services.trading_service.API')
@patch('src.services.trading_service.CALC')
def test_execute_market_buy(mock_calc, mock_api):
    # Setup
    mock_api.F_Get_Symbol_Info.return_value = "0.00001000" # Min/Max Qty
    mock_calc.F_Virtual_Quantity.return_value = "0.123"
    
    # Run
    result = TRADE.execute_market_buy("BTC", 0.5)
    
    # Verify
    assert result == True
    mock_api.F_Get_Binance.return_value.order_market.assert_called_with(
        symbol="BTCUSDT", side="BUY", quantity="0.123"
    )

@patch('src.services.trading_service.API')
def test_execute_market_buy_failure(mock_api):
    mock_api.F_Get_Symbol_Info.return_value = "0.00001000"
    # Simulate API Exception
    mock_api.F_Get_Binance.return_value.order_market.side_effect = Exception("API Error")
    
    # Call
    # Note: CALC is imported in module, if we don't mock it, it runs real logic.
    # We need to ensure F_Virtual_Quantity returns something valid or mock it.
    # If not mocked, it might log warning or return None if inputs bad.
    # Here inputs are fine.
    
    with patch('src.services.trading_service.CALC.F_Virtual_Quantity', return_value="0.1"):
        result = TRADE.execute_market_buy("BTC", 0.1)
        assert result == False
# endregion
