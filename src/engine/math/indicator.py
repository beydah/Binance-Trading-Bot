# ----------------------------------------------------------------
# Added Links
# DATA
from src.engine.data import data as DATA
from src.engine.data import write as WRITE
from src.engine.data import read as READ
# MATH
from src.engine.math import calculator as CALCULATE
from src.engine.math import trade as TRADE
# MESSAGE
from src.engine.message import bot as BOT
from src.engine.message import message as MESSAGE
from src.engine.message import transactions as TRANSACTIONS
# SETTING
from src.engine.settings import api as API
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# THREAD
from src.engine.thread import timer as TIMER
from src.engine.thread import debugger as DEBUGGER
from src.engine.thread import processor as PROCESSOR
# ----------------------------------------------------------------


# Indicator Calculations
def SMA(MA_LENGTH, CLOSE_PRICE): return LIB.TA.ma("sma", CLOSE_PRICE, length=MA_LENGTH)


def EMA(MA_LENGTH, CLOSE_PRICE): return LIB.TA.ema(name="ema", close=CLOSE_PRICE, length=MA_LENGTH)


def RSI(CLOSE_PRICE): return LIB.TA.rsi(CLOSE_PRICE, DEF.RSI_LENGTH)


def STOCHRSI(CLOSE_PRICE):
    stochRSI = LIB.TA.stochrsi(CLOSE_PRICE, DEF.STOCHRSI_STOCH_LENGTH, DEF.STOCHRSI_RSI_LENGTH,
                               DEF.STOCHRSI_SMOOTH_K, DEF.STOCHRSI_SMOOTH_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI["stochRSI_K"]


def GOLDENFIVE(OLD_PRICE, PRICE, OLD_SMA25, SMA25, OLD_SMA50, SMA50,
               OLD_SMA200, SMA200, OLD_EMA25, EMA25, RSI_NUM, STOCHRSI_NUM):
    dcaSignal = DCA_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25)
    emaSignal = DCA_SIGNAL(OLD_PRICE, PRICE, OLD_EMA25, EMA25)
    goldenCrossSignal = GOLDENCROSS_SIGNAL(OLD_SMA50, SMA50, OLD_SMA200, SMA200)
    rsiSignal = RSI_SIGNAL(RSI_NUM)
    stochRSISignal = RSI_SIGNAL(STOCHRSI_NUM)
    indicatorSignals = [dcaSignal, emaSignal, goldenCrossSignal, rsiSignal, stochRSISignal]
    signalBuy = signalSell = 0
    for signal in indicatorSignals:
        if signal == 1: signalBuy += 1
        elif signal == -1: signalSell += 1
    goldenNums = [signalBuy, signalSell]
    return goldenNums
# ----------------------------------------------------------------


# Signal Calculations
def DCA_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25):
    if OLD_PRICE < OLD_SMA25 and PRICE > SMA25: return 1
    if OLD_PRICE > OLD_SMA25 and PRICE < SMA25: return -1
    return 0


def GOLDENCROSS_SIGNAL(OLD_SMA50, SMA50, OLD_SMA200, SMA200):
    if OLD_SMA50 < OLD_SMA200 and SMA50 > SMA200: return 1
    if OLD_SMA50 > OLD_SMA200 and SMA50 < SMA200: return -1
    return 0


def RSI_SIGNAL(RSI_NUM):
    if RSI_NUM < 30: return 1
    if RSI_NUM > 70: return -1
    return 0


def GOLDENFIVE_SIGNAL(GOLDEN_NUMS):
    if GOLDEN_NUMS[0] > 2: return 1
    if GOLDEN_NUMS[1] > 2: return -1
    return 0
# ----------------------------------------------------------------
