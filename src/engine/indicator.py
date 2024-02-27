# ----------------------------------------------------------------
# Added Links
from src.engine import dataops as DATA
from src.settings import library as LIB
from src.settings import settings as DEF
# ----------------------------------------------------------------


# Indicator Calculations
def SMA(MA_LENGTH, COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    sma = LIB.TA.ma("sma", CLOSE_PRICE, length=MA_LENGTH)
    return sma


def EMA(MA_LENGTH, COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    ema = LIB.TA.ema(name="ema", close=CLOSE_PRICE, length=MA_LENGTH)
    return ema


def RSI(COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    rsi = LIB.TA.rsi(CLOSE_PRICE, DEF.RSI_LENGTH)
    return rsi


def STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, None, None, 4)
    stochRSI = LIB.TA.stochrsi(CLOSE_PRICE, DEF.STOCHRSI_STOCH_LENGTH, DEF.STOCHRSI_RSI_LENGTH,
                               DEF.STOCHRSI_SMOOTH_K, DEF.STOCHRSI_SMOOTH_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI


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
    goldenFiveNums = [signalBuy, signalSell]
    return goldenFiveNums
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
    signalBuy = GOLDEN_NUMS[0]
    signalSell = GOLDEN_NUMS[1]
    signalLimit = 3
    if signalBuy >= signalLimit: return 1
    if signalSell >= signalLimit: return -1
    return 0


def FIVEPERIOD_SIGNAL(COIN_SYMBOL, DATETIME):
    signalBuy = signalSell = 0
    signalLimit = 2
    for period in DEF.CANDLE_PEROIDS:
        closePrice = DATA.READ_CANDLE(COIN_SYMBOL, period, DATETIME, 250, 4)
        sma25 = SMA(DEF.MA_LENGTHS[0], COIN_SYMBOL, None, closePrice)
        ema25 = EMA(DEF.MA_LENGTHS[0], COIN_SYMBOL, None, closePrice)
        sma50 = SMA(DEF.MA_LENGTHS[1], COIN_SYMBOL, None, closePrice)
        sma200 = SMA(DEF.MA_LENGTHS[2], COIN_SYMBOL, None, closePrice)
        rsi = RSI(COIN_SYMBOL, None, closePrice)
        stochRSI = STOCHRSI(COIN_SYMBOL, None, closePrice)
        stochRSI_K = stochRSI["stochRSI_K"]
        past = len(closePrice) - 3
        last = len(closePrice) - 2
        if not any(LIB.PD.isna([sma25[past], sma50[past], sma200[past], rsi[past], stochRSI_K[past]])):
            goldenNums = GOLDENFIVE(closePrice[past], closePrice[last], sma25[past], sma25[last],
                                    sma50[past], sma50[last], sma200[past], sma200[last],
                                    ema25[past], ema25[last], rsi[last], stochRSI_K[last])
            signal = GOLDENFIVE_SIGNAL(goldenNums)
        else: signal = 0
        if signal == 1: signalBuy += 1
        elif signal == -1: signalSell += 1
    if signalBuy == signalSell: return 0
    if signalBuy >= signalLimit: return 1
    if signalSell >= signalLimit: return -1
    return 0
# ----------------------------------------------------------------
