# Added Pages
from src.settings import settings as S
from src.business import business as B
# ----------------------------------------------------------------


# Indicator Calculations
def STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 4)
    stochRSI = S.TA.stochrsi(closePrice, S.STOCHRSI_STOCH_LENGTH,
                             S.STOCHRSI_RSI_LENGTH, S.STOCHRSI_SMOOTH_K, S.STOCHRSI_SMOOTH_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI


def RSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 4)
    rsi = S.TA.rsi(closePrice, S.RSI_LENGTH)
    return rsi


def MACD(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 4)
    macd = S.TA.macd(closePrice, S.MACD_FAST, S.MACD_SLOW, S.MACD_SIGNAL)
    return macd


def BOLL(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 4)
    boll = S.TA.bbands(closePrice, S.BOLL_LENGTH)
    return boll


def SMA(COIN_SYMBOL, CANDLE_PERIOD, MA_LENGTH, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 4)
    sma = S.TA.ma("sma", closePrice, length=MA_LENGTH)
    return sma


def EMA(COIN_SYMBOL, CANDLE_PERIOD, MA_LENGTH, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 4)
    ema = S.TA.ema("ema", closePrice, length=MA_LENGTH)
    return ema
# ----------------------------------------------------------------
