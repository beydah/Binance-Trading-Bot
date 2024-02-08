from src.business import backtest as TEST

'''
"BTC", "ETH", "BNB", "USDT", "PAXG", "TRY"
"1d", "4h", "1h", "15m", "5m"]
'''
TEST.BASIC_STOCHRSI_ALGORITHM("BTC", "USDT", "1d", 1000)
