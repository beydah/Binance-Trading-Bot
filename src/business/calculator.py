from src.business import business as B
from src.settings import settings as S
import pandas_ta as TA


def RSI(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = B.RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        rsi = TA.rsi(closePrice, S.RSI_LENGTH)
        return rsi
    except Exception:
        print("ERROR - CALCULATE_RSI: Couldn't Calculate RSI")
        return -1


def MA(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = B.RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        ma = TA.ma("sma", closePrice, length=S.MA_LENGTH)
        return ma
    except Exception:
        print("ERROR - CALCULATE_MA: Couldn't Calculate MA")
        return -1


def EMA(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = B.RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        ema = TA.ema("ema", closePrice, length=S.MA_LENGTH)
        return ema
    except Exception:
        print("ERROR - CALCULATE_EMA: Couldn't Calculate EMA")
        return -1


def STOCHRSI(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = B.RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        stochRSI = TA.stochrsi(closePrice, S.STOCHRSI_STOCH_LENGTH,
                               S.STOCHRSI_RSI_LENGTH, S.STOCHRSI_SMOOTH_K, S.STOCHRSI_SMOOTH_D)
        return stochRSI
    except Exception:
        print("ERROR - CALCULATE_STOCHRSI: Couldn't Calculate STOCHRSI")
        return -1


def MACD(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = B.RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        macd = TA.macd(closePrice, S.MACD_FAST, S.MACD_SLOW, S.MACD_SIGNAL)
        return macd
    except Exception:
        print("ERROR - CALCULATE_MACD: Couldn't Calculate MACD")
        return -1


def BOLL(SYMBOL_ID, PERIOD_ID):
    try:
        closePrice = B.RETURN_CANDLE_SYMBOLS(SYMBOL_ID, PERIOD_ID, 4)
        boll = TA.bbands(closePrice, S.BOLL_LENGTH)
        return boll
    except Exception:
        print("ERROR - CALCULATE_BOLL: Couldn't Calculate BOLL")
        return -1
