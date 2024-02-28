# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import algotest as TEST
from src.engine import calculator as CALCULATE
from src.engine import signal as SIGNAL

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Indicator Calculations
def SMA(MA_LENGTH, COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = CANDLE.READ(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    sma = LIB.TA.ma("sma", CLOSE_PRICE, length=MA_LENGTH)
    return sma


def EMA(MA_LENGTH, COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = CANDLE.READ(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    ema = LIB.TA.ema(name="ema", close=CLOSE_PRICE, length=MA_LENGTH)
    return ema


def RSI(COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = CANDLE.READ(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    rsi = LIB.TA.rsi(CLOSE_PRICE, DEF.RSI_LENGTH)
    return rsi


def STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = CANDLE.READ(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    stochRSI = LIB.TA.stochrsi(CLOSE_PRICE, DEF.STOCHRSI_STOCH_LENGTH, DEF.STOCHRSI_RSI_LENGTH,
                               DEF.STOCHRSI_SMOOTH_K, DEF.STOCHRSI_SMOOTH_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI


def GOLDENFIVE(OLD_PRICE, PRICE, OLD_SMA25, SMA25, OLD_SMA50, SMA50,
               OLD_SMA200, SMA200, OLD_EMA25, EMA25, RSI_NUM, STOCHRSI_NUM):
    dcaSignal = SIGNAL.DCA(OLD_PRICE, PRICE, OLD_SMA25, SMA25)
    emaSignal = SIGNAL.DCA(OLD_PRICE, PRICE, OLD_EMA25, EMA25)
    goldenCrossSignal = SIGNAL.GOLDENCROSS(OLD_SMA50, SMA50, OLD_SMA200, SMA200)
    rsiSignal = SIGNAL.RSI(RSI_NUM)
    stochRSISignal = SIGNAL.RSI(STOCHRSI_NUM)
    indicatorSignals = [dcaSignal, emaSignal, goldenCrossSignal, rsiSignal, stochRSISignal]
    signalBuy = signalSell = 0
    for signal in indicatorSignals:
        if signal == 1: signalBuy += 1
        elif signal == -1: signalSell += 1
    goldenFiveNums = [signalBuy, signalSell]
    return goldenFiveNums
# ----------------------------------------------------------------
