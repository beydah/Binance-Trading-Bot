from src.settings import settings as S

import csv as CSV
import os as OS

import pandas as PD

from binance import Client as BINANCE
from datetime import datetime as DT

CLIENT = BINANCE(S.API_KEY, S.API_SECRET)


def CANDLE_GET_SYMBOLS(COIN_SYMBOL, CANDLE_PERIOD):
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD, limit=S.CANDLE_LIMIT)
    return candleList


def WRITE_CANDLE_ON_CSV_SYMBOLS(COIN_SYMBOL, CANDLE_PERIOD):
    try:
        if not OS.path.exists("../data"): OS.makedirs("../data")
        folderPath = OS.path.join("../data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
        with open(folderPath, "w", newline='') as csvFile:
            writer = CSV.writer(csvFile, delimiter=',')
            for candleData in CANDLE_GET_SYMBOLS(COIN_SYMBOL, CANDLE_PERIOD):
                candleData[0] = TIMESET(candleData[0])
                candleData[6] = TIMESET(candleData[6])
                writer.writerow(candleData)
        csvFile.close()
    except Exception:
        print("ERROR - WRITE_CANDLE_ON_CSV_SYMBOLS: File Could Not Be Created")
        return -1


def RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, HEAD_ID):
    try:
        coinSymbol = S.COIN_SYMBOLS[SYMBOL_ID]
        candlePeriod = S.CANDLE_PEROIDS[PERIOD_ID]
        WRITE_CANDLE_ON_CSV_SYMBOLS(coinSymbol, candlePeriod)
        readCSV = OS.path.join("../data", f"{coinSymbol}_{candlePeriod}.csv")
        with open(readCSV, "r", newline='') as csvFile:
            headers = \
                ['Open_Time', 'Open_Price', 'High_Price', 'Low_Price', 'Close_Price',
                 'Volume', 'Close_Time', 'QAV', 'NAT', 'TBBAV', 'TBQAV', 'Ignore']
            df = PD.read_csv(readCSV, names=headers)
        csvFile.close()
        if HEAD_ID == -1:
            return df
        elif HEAD_ID > -1 and HEAD_ID < 12:
            header = headers[HEAD_ID]
            return df[header]
        else:
            return "Unknown HEAD_ID"
    except Exception:
        print("ERROR - RETURN_CANDLE_SYMBOLS: Couldn't Read File")
        return -1


def TIMESET(TIMESTAMP):
    try:
        return DT.fromtimestamp(TIMESTAMP / 1000)
    except Exception:
        print("ERROR - TIMESET: Couldn't Convert Timestamp")
        return -1
