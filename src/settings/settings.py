# ----------------------------------------------------------------
# Added Libraries
from binance import Client as BINANCE
import telebot as BOT
from telebot import types as TYPES
import requests as REQUEST
import csv as CSV
import os as OS
import heapq as HEAP
import pandas as PD
import pandas_ta as TA
from datetime import datetime as TIME
from datetime import timedelta as TD
# ----------------------------------------------------------------
# Indicator SettingS
STOCHRSI_RSI_LENGTH = 11
STOCHRSI_STOCH_LENGTH = 11
STOCHRSI_SMOOTH_K = 11
STOCHRSI_SMOOTH_D = 11
RSI_LENGTH = 11  # 11
MA_LENGTHS = [25, 50, 200]
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLL_LENGTH = 20
BOLL_STD = 2
# ----------------------------------------------------------------
# Other Settings
CANDLE_PEROIDS = ["8h", "4h", "2h", "1h", "15m"]
CHANGELIST_DAYS = [1, 7, 30, 90, 180, 365]
BINANCE_COMISSION_RATE = 0.1 / 100
# ----------------------------------------------------------------
