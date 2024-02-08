from src.business import business as B
from src.settings import settings as S


def RSI(COIN_SYMBOL, CANDLE_PERIOD):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, 4)
    rsi = B.TA.rsi(closePrice, S.RSI_LENGTH)
    return rsi


def STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, 4)
    stochRSI = B.TA.stochrsi(closePrice, S.STOCHRSI_STOCH_LENGTH,
                             S.STOCHRSI_RSI_LENGTH, S.STOCHRSI_SMOOTH_K, S.STOCHRSI_SMOOTH_D)
    return stochRSI


def SMA(SYMBOL, PERIOD, MA_LENGTH):
    closePrice = B.READ_CANDLE(SYMBOL, PERIOD, 4)
    sma = B.TA.ma("sma", closePrice, length=MA_LENGTH)
    return sma


def EMA(SYMBOL, PERIOD, MA_LENGTH):
    closePrice = B.READ_CANDLE(SYMBOL, PERIOD, 4)
    ema = B.TA.ema("ema", closePrice, length=MA_LENGTH)
    return ema


def MACD(COIN_SYMBOL, CANDLE_PERIOD):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, 4)
    macd = B.TA.macd(closePrice, S.MACD_FAST, S.MACD_SLOW, S.MACD_SIGNAL)
    return macd


def BOLL(COIN_SYMBOL, CANDLE_PERIOD):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, 4)
    boll = B.TA.bbands(closePrice, S.BOLL_LENGTH)
    return boll
