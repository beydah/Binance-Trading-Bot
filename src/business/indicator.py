# ----------------------------------------------------------------
# Added Links
from src.business import business as B
from src.business import calculator as CALCULATE
from src.business import backtest as TEST
from src.settings import settings as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Indicator Calculations
def SMA(COIN_SYMBOL, CANDLE_PERIOD, MA_LENGTH, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 1000, 4)
    sma = LIB.TA.ma("sma", closePrice, length=MA_LENGTH)
    return sma


def EMA(COIN_SYMBOL, CANDLE_PERIOD, MA_LENGTH, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 1000, 4)
    ema = LIB.TA.ema(name="ema", close=closePrice, length=MA_LENGTH)
    return ema


def RSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 1000, 4)
    rsi = LIB.TA.rsi(closePrice, LIB.RSI_LENGTH)
    return rsi


def STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 1000, 4)
    stochRSI = LIB.TA.stochrsi(closePrice, LIB.STOCHRSI_STOCH_LENGTH,
                               LIB.STOCHRSI_RSI_LENGTH, LIB.STOCHRSI_SMOOTH_K, LIB.STOCHRSI_SMOOTH_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI


def MACD(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 1000, 4)
    macd = LIB.TA.macd(closePrice, LIB.MACD_FAST, LIB.MACD_SLOW, LIB.MACD_SIGNAL)
    return macd


def BOLL(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None):
    closePrice = B.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 1000, 4)
    boll = LIB.TA.bbands(closePrice, LIB.BOLL_LENGTH)
    return boll
# ----------------------------------------------------------------


# Signal Calculations
def DCA_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25):
    if OLD_PRICE < OLD_SMA25 and PRICE > SMA25: return 1
    elif OLD_PRICE > OLD_SMA25 and PRICE < SMA25: return -1
    else: return 0


def EMA_SIGNAL(OLD_PRICE, PRICE, OLD_EMA, EMA_NUM):
    if OLD_PRICE < OLD_EMA and PRICE > EMA_NUM: return 1
    elif OLD_PRICE > OLD_EMA and PRICE < EMA_NUM: return -1
    else: return 0


def GOLDENCROSS_SIGNAL(OLD_SMA50, OLD_SMA200, SMA50, SMA200):
    if OLD_SMA50 < OLD_SMA200 and SMA50 > SMA200: return 1
    elif OLD_SMA50 > OLD_SMA200 and SMA50 < SMA200: return -1
    else: return 0


def RSI_SIGNAL(RSI_NUM):
    if RSI_NUM < 30: return 1
    elif RSI_NUM > 70: return -1
    else: return 0


def STOCHRSI_SIGNAL(STOCHRSI_NUM):
    if STOCHRSI_NUM < 30: return 1
    elif STOCHRSI_NUM > 70: return -1
    else: return 0


def MIX_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25, OLD_SMA50, SMA50,
               OLD_SMA200, SMA200, OLD_EMA25, EMA25, STOCHRSI_NUM, RSI_NUM):
    signalBuy = 0
    signalSell = 0
    signalLimit = 3
    if DCA_SIGNAL(OLD_PRICE, OLD_SMA25, PRICE, SMA25) == 1: signalBuy += 1
    elif DCA_SIGNAL(OLD_PRICE, OLD_SMA25, PRICE, SMA25) == -1: signalSell += 1
    if GOLDENCROSS_SIGNAL(OLD_SMA50, OLD_SMA200, SMA50, SMA200) == 1: signalBuy += 1
    elif GOLDENCROSS_SIGNAL(OLD_SMA50, OLD_SMA200, SMA50, SMA200) == -1: signalSell += 1
    if EMA_SIGNAL(OLD_PRICE, OLD_EMA25, PRICE, EMA25) == 1: signalBuy += 1
    elif EMA_SIGNAL(OLD_PRICE, OLD_EMA25, PRICE, EMA25) == -1: signalSell += 1
    if STOCHRSI_SIGNAL(STOCHRSI_NUM) == 1: signalBuy += 1
    elif STOCHRSI_SIGNAL(STOCHRSI_NUM) == -1: signalSell += 1
    if RSI_SIGNAL(RSI_NUM) == 1: signalBuy += 1
    elif RSI_SIGNAL(RSI_NUM) == -1: signalSell += 1
    if signalBuy >= signalLimit: return 1
    elif signalSell >= signalLimit: return -1
    else: return 0
# ----------------------------------------------------------------
