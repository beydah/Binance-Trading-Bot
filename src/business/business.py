from src.settings import settings as S
from src.settings import api as API

import csv as CSV
import os as OS

import pandas as PD
import pandas_ta as TA

import requests as REQUEST
import telebot as BOT
from telebot import types as TYPES

from binance import Client as BINANCE
from datetime import datetime as DT

CLIENT = BINANCE(API.BINANCE_KEY, API.BINANCE_SECRET)
TELEGRAM_BOT = BOT.TeleBot(API.TELEGRAM_BOT_KEY)


def GET_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD, limit=S.CANDLE_LIMIT)
    return candleList


def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    if not OS.path.exists("../data"): OS.makedirs("../data")
    folderPath = OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(folderPath, "w", newline='') as csvFile:
        writer = CSV.writer(csvFile, delimiter=',')
        for candleData in GET_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
            candleData[0] = TIMESET(candleData[0])
            candleData[6] = TIMESET(candleData[6])
            writer.writerow(candleData)
    csvFile.close()


def READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, HEAD_ID):
    WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    readCSV = OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(readCSV, "r", newline='') as csvFile:
        headers = \
            ["Open_Time", "Open_Price", "High_Price", "Low_Price", "Close_Price",
             "Volume", "Close_Time", "QAV", "NAT", "TBBAV", "TBQAV", "Ignore"]
        df = PD.read_csv(readCSV, names=headers)
    csvFile.close()
    if HEAD_ID == -1:
        return df
    elif -1 < HEAD_ID < 12:
        header = headers[HEAD_ID]
        return df[header]
    else:
        return "Unknown HEAD_ID"


def GET_SYMBOL_FROM_ID(SYMBOL_ID):
    coinSymbol = S.COIN_SYMBOLS[SYMBOL_ID]
    return coinSymbol


def GET_PERIOD_FROM_ID(PERIOD_ID):
    candlePeriod = S.CANDLE_PEROIDS[PERIOD_ID]
    return candlePeriod


def COMBINE_SYMBOL(LEFT_SYMBOL, RIGHT_SYMBOL):
    combinerSymbol = LEFT_SYMBOL + RIGHT_SYMBOL
    return combinerSymbol


def TIMESET(TIMESTAMP):
    return DT.fromtimestamp(TIMESTAMP / 1000)


def BOT_MESSAGE_SEND(BOT_MESSAGE):
    URL = \
        (f"https://api.telegram.org/bot{API.TELEGRAM_BOT_TOKEN}"
         f"/sendMessage?chat_id={API.TELEGRAM_USER_ID}"
         f"&parse_mode=Markdown&text={BOT_MESSAGE}")
    REQUEST.get(URL)
