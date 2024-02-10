# Added Libraries
from binance import Client as BINANCE
import csv as CSV
import os as OS
from datetime import datetime as TIME
import pandas as PD
import pandas_ta as TA
import telebot as BOT
import requests as REQUEST
from telebot import types as TYPES
# ----------------------------------------------------------------
# Indicator Settings
STOCHRSI_RSI_LENGTH = 5
STOCHRSI_STOCH_LENGTH = 5
STOCHRSI_SMOOTH_K = 5
STOCHRSI_SMOOTH_D = 5
RSI_LENGTH = 14
MA_LENGTHS = [25, 50, 200]
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLL_LENGTH = 20
BOLL_STD = 2
# ----------------------------------------------------------------
# Other Settings
COIN_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"]
CANDLE_PEROIDS = ["1d", "8h", "4h", "1h", "15m"]
BINANCE_COMISSION_RATE = 0.1 / 100
CANDLE_LIMIT = 1000
# ----------------------------------------------------------------
