# ----------------------------------------------------------------
# Added Links
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


# Indicator Calculations
def SMA(MA_Length, Prices): return LIB.TA.ma("sma", Prices, length=MA_Length)


def EMA(MA_Length, Prices): return LIB.TA.ema(name="ema", close=Prices, length=MA_Length)


def RSI(Prices): return LIB.TA.rsi(Prices, DEF.RSI_Length)


def STOCHRSI(Prices):
    stochRSI = LIB.TA.stochrsi(Prices, DEF.StochRSI_Stoch_Length, DEF.StochRSI_Length,
                               DEF.StochRSI_Smooth_K, DEF.StochRSI_Smooth_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI["stochRSI_K"]


def GOLDENFIVE(Old_Prices, Prices, Old_SMA25, SMA25, Old_SMA50, SMA50,
               Old_SMA200, SMA200, Old_EMA25, EMA25, RSI_Num, StochRSI_Num):
    DCA_signal = DCA_SIGNAL(Old_Prices, Prices, Old_SMA25, SMA25)
    EMA_signal = DCA_SIGNAL(Old_Prices, Prices, Old_EMA25, EMA25)
    golden_cross_signal = GOLDENCROSS_SIGNAL(Old_SMA50, SMA50, Old_SMA200, SMA200)
    RSI_signal = RSI_SIGNAL(RSI_Num)
    stochRSI_signal = RSI_SIGNAL(StochRSI_Num)
    indicator_signals = [DCA_signal, EMA_signal, golden_cross_signal, RSI_signal, stochRSI_signal]
    signal_buy = signal_sell = 0
    for signal in indicator_signals:
        if signal == 1: signal_buy += 1
        elif signal == -1: signal_sell += 1
    return [signal_buy, signal_sell]
# ----------------------------------------------------------------


# Signal Calculations
def DCA_SIGNAL(Old_Prices, Prices, Old_SMA25, SMA25):
    if Old_Prices < Old_SMA25 and Prices > SMA25: return 1
    if Old_Prices > Old_SMA25 and Prices < SMA25: return -1
    return 0


def GOLDENCROSS_SIGNAL(Old_SMA50, SMA50, Old_SMA200, SMA200):
    if Old_SMA50 < Old_SMA200 and SMA50 > SMA200: return 1
    if Old_SMA50 > Old_SMA200 and SMA50 < SMA200: return -1
    return 0


def RSI_SIGNAL(RSI_Num):
    if RSI_Num < 30: return 1
    if RSI_Num > 70: return -1
    return 0


def GOLDENFIVE_SIGNAL(Golden_Num):
    if Golden_Num[0] > 2: return 1
    if Golden_Num[1] > 2: return -1
    return 0
# ----------------------------------------------------------------
