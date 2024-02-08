from src.settings import settings as S

import csv as CSV
import os as OS

import pandas as PD
import pandas_ta as TA

from binance import Client as BINANCE
from datetime import datetime as DT

CLIENT = BINANCE(S.API_KEY, S.API_SECRET)


def GET_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD, limit=S.CANDLE_LIMIT)
    return candleList


def WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
    if not OS.path.exists("../data"): OS.makedirs("../data")
    folderPath = OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(folderPath, "w", newline='') as csvFile:
        writer = CSV.writer(csvFile, delimiter=',')
        for candleData in GET_CANDLE(COIN_SYMBOL, CANDLE_PERIOD):
            candleData[0] = SET_TIME(candleData[0])
            candleData[6] = SET_TIME(candleData[6])
            writer.writerow(candleData)
    csvFile.close()


def READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, HEAD_ID):
    WRITE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    readCSV = OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
    with open(readCSV, "r", newline='') as csvFile:
        headers = \
            ['Open_Time', 'Open_Price', 'High_Price', 'Low_Price', 'Close_Price',
             'Volume', 'Close_Time', 'QAV', 'NAT', 'TBBAV', 'TBQAV', 'Ignore']
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


def GET_MA_LENGTH_FROM_ID(MA_LENGTH_ID):
    maLength = S.MA_LENGTHS[MA_LENGTH_ID]
    return maLength


def COMBINE_SYMBOL(LEFT_SYMBOL, RIGHT_SYMBOL):
    combinerSymbol = LEFT_SYMBOL + RIGHT_SYMBOL
    return combinerSymbol


def SET_TIME(TIMESTAMP):
    return DT.fromtimestamp(TIMESTAMP / 1000)
