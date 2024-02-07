import settings as S

import csv as CSV
import os as OS

import pandas as PD
import pandas_ta as TA

from binance import Client as BINANCE
from datetime import datetime as DT

################################################################
COIN_SYMBOLS = S.COIN_SYMBOLS
CANDLE_PEROIDS = S.CANDLE_PEROIDS
CANDLE_LIMIT = S.CANDLE_LIMIT

RSI_LENGTH = S.RSI_LENGTH
MA_LENGTH = S.MA_LENGTH
MACD_FAST = S.MACD_FAST
MACD_SLOW = S.MACD_SLOW
MACD_SIGNAL = S.MACD_SIGNAL
BOLL_LENGTH = S.BOLL_LENGTH
BOLL_STD = S.BOLL_STD

STOCHRSI_RSI_LENGTH = S.STOCHRSI_RSI_LENGTH
STOCHRSI_STOCH_LENGTH = S.STOCHRSI_STOCH_LENGTH
STOCHRSI_SMOOTH_K = S.STOCHRSI_SMOOTH_K
STOCHRSI_SMOOTH_D = S.STOCHRSI_SMOOTH_D

API_KEY = S.BINANCE_API_KEY
API_SECRET = S.BINANCE_API_SECRET

CLIENT = BINANCE(API_KEY, API_SECRET)


################################################################
def CANDLE_GET_SYMBOLS(COIN_SYMBOL, CANDLE_PERIOD):
    candleList = CLIENT.get_historical_klines(symbol=COIN_SYMBOL, interval=CANDLE_PERIOD, limit=CANDLE_LIMIT)
    return candleList


def WRITE_CANDLE_ON_CSV_SYMBOLS(COIN_SYMBOL, CANDLE_PERIOD):
    try:
        if not OS.path.exists("data"): OS.makedirs("data")
        folderPath = OS.path.join("data", f"{COIN_SYMBOL}_{CANDLE_PERIOD}.csv")
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
        coinSymbol = COIN_SYMBOLS[SYMBOL_ID]
        candlePeriod = CANDLE_PEROIDS[PERIOD_ID]
        WRITE_CANDLE_ON_CSV_SYMBOLS(coinSymbol, candlePeriod)
        readCSV = OS.path.join("data", f"{coinSymbol}_{candlePeriod}.csv")
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


################################################################
def CALCULATE_RSI(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        rsi = TA.rsi(closePrice, RSI_LENGTH)
        return rsi
    except Exception:
        print("ERROR - CALCULATE_RSI: Couldn't Calculate RSI")
        return -1


def CALCULATE_MA(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        ma = TA.ma("sma", closePrice, length=MA_LENGTH)
        return ma
    except Exception:
        print("ERROR - CALCULATE_MA: Couldn't Calculate MA")
        return -1


def CALCULATE_EMA(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        ema = TA.ema("ema", closePrice, length=MA_LENGTH)
        return ema
    except Exception:
        print("ERROR - CALCULATE_EMA: Couldn't Calculate EMA")
        return -1


def CALCULATE_STOCHRSI(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        stochRSI = TA.stochrsi(closePrice, STOCHRSI_STOCH_LENGTH,
                               STOCHRSI_RSI_LENGTH, STOCHRSI_SMOOTH_K, STOCHRSI_SMOOTH_D)
        return stochRSI
    except Exception:
        print("ERROR - CALCULATE_STOCHRSI: Couldn't Calculate STOCHRSI")
        return -1


def CALCULATE_MACD(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        macd = TA.macd(closePrice, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
        return macd
    except Exception:
        print("ERROR - CALCULATE_MACD: Couldn't Calculate MACD")
        return -1


def CALCULATE_BOLL(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        boll = TA.bbands(closePrice, BOLL_LENGTH)
        return boll
    except Exception:
        print("ERROR - CALCULATE_BOLL: Couldn't Calculate BOLL")
        return -1


################################################################
def TEST_DCA_ALGORITHM(SMYBOL_ID, PERIOD_ID, DOLLAR_PER_TRANSACTION):
    try:
        purchasesNum = 0
        totalCoin = 0
        commission = 0
        commissionRate = 1 / 10

        symbol = COIN_SYMBOLS[SMYBOL_ID]
        openTime = RETURN_CANDLE_SYMBOLS(SMYBOL_ID, PERIOD_ID, 0)
        closePrice = RETURN_CANDLE_SYMBOLS(SMYBOL_ID, PERIOD_ID, 4)

        sma = CALCULATE_MA(SMYBOL_ID, PERIOD_ID)

        for i in range(len(closePrice)):
            if PD.isna(sma[i]) is False:
                if closePrice[i - 1] < sma[i - 1] and closePrice[i] > sma[i]:
                    print(DOLLAR_PER_TRANSACTION / closePrice[i], " ", symbol, " Received on ", openTime[i + 1])
                    print("####################################################")
                    purchasesNum += 1
                    totalCoin += DOLLAR_PER_TRANSACTION / closePrice[i]
                    commission += commissionRate * DOLLAR_PER_TRANSACTION

        print("Total Transactions: ", purchasesNum)
        print("Total Received ", symbol, ": ", totalCoin)
        print("Total Investment: ", purchasesNum * DOLLAR_PER_TRANSACTION, " Dollar")
        print("Current Wallet: ", totalCoin * closePrice[len(closePrice) - 1] - commission, " Dollar")
    except Exception:
        print("ERROR - TEST_DCA_ALGORITHM: Couldn't Test DCA Algorithm")
        return -1
################################################################
