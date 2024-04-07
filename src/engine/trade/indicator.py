# ----------------------------------------------------------------
# Added Links
from src.engine.settings import library as LIB
from src.engine.settings import settings as DEF
# ----------------------------------------------------------------


def SMA(MA_Length, Prices): return LIB.TA.ma("sma", Prices, length=MA_Length)


def EMA(MA_Length, Prices): return LIB.TA.ema(name="ema", close=Prices, length=MA_Length)


def RSI(Prices): return LIB.TA.rsi(Prices, DEF.RSI_Length)


def STOCH_RSI(Prices):
    settings = [DEF.StochRSI_Stoch_Length, DEF.StochRSI_Length, DEF.StochRSI_Smooth_K, DEF.StochRSI_Smooth_D]
    stochRSI = LIB.TA.stochrsi(Prices, settings[0], settings[1], settings[2], settings[3])
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI["stochRSI_K"]


def GOLDEN_FIVE(Prices):
    full_signals = FULL_SIGNALS(Prices)
    signal_buy = signal_sell = 0
    for signal in full_signals:
        if signal == 1: signal_buy += 1
        elif signal == -1: signal_sell += 1
    return [signal_buy, signal_sell]


def GOLDEN_FIVE_TEST(Old_Price, Price, Old_EMA25, EMA25, Old_SMA25, SMA25,
                     Old_SMA50, SMA50, Old_SMA200, SMA200, RSI_Num, Stoch_RSI_Num):
    ema_signal = DCA_SIGNAL(Old_Price, Price, Old_EMA25, EMA25)
    dca_signal = DCA_SIGNAL(Old_Price, Price, Old_SMA25, SMA25)
    golden_cross_signal = GOLDEN_CROSS_SIGNAL(Old_SMA50, SMA50, Old_SMA200, SMA200)
    rsi_signal = RSI_SIGNAL(RSI_Num)
    stoch_rsi_signal = RSI_SIGNAL(Stoch_RSI_Num)
    indicator_signals = [ema_signal, dca_signal, golden_cross_signal, rsi_signal, stoch_rsi_signal]
    signal_buy = signal_sell = 0
    for signal in indicator_signals:
        if signal == 1: signal_buy += 1
        elif signal == -1: signal_sell += 1
    return [signal_buy, signal_sell]
# ----------------------------------------------------------------

def DCA_SIGNAL(Old_Prices, Prices, Old_SMA25, SMA25):
    if Old_Prices < Old_SMA25 and Prices > SMA25: return 1
    if Old_Prices > Old_SMA25 and Prices < SMA25: return -1
    return 0


def GOLDEN_CROSS_SIGNAL(Old_SMA50, SMA50, Old_SMA200, SMA200):
    if Old_SMA50 < Old_SMA200 and SMA50 > SMA200: return 1
    if Old_SMA50 > Old_SMA200 and SMA50 < SMA200: return -1
    return 0


# TODO: TEST
"""
def DCA_SIGNAL(Old_Prices, Prices, Old_SMA25, SMA25):
    if Prices > SMA25: return 1
    if Prices < SMA25: return -1
    return 0


def GOLDEN_CROSS_SIGNAL(Old_SMA50, SMA50, Old_SMA200, SMA200):
    if SMA50 > SMA200: return 1
    if SMA50 < SMA200: return -1
    return 0
"""

def RSI_SIGNAL(RSI_Num):
    if RSI_Num < 30: return 1
    if RSI_Num > 70: return -1
    return 0


def FULL_SIGNALS(Prices):
    ema25 = EMA(MA_Length=DEF.MA_Lengths[0], Prices=Prices)
    sma25 = SMA(MA_Length=DEF.MA_Lengths[0], Prices=Prices)
    sma50 = SMA(MA_Length=DEF.MA_Lengths[1], Prices=Prices)
    sma200 = SMA(MA_Length=DEF.MA_Lengths[2], Prices=Prices)
    rsi = RSI(Prices)
    stochRSI = STOCH_RSI(Prices)
    last = len(Prices) - 2
    indicator_signal = [0] * 5
    indicator_signal[0] = DCA_SIGNAL(Prices[last - 1], Prices[last], ema25[last - 1], ema25[last])
    indicator_signal[1] = DCA_SIGNAL(Prices[last - 1], Prices[last], sma25[last - 1], sma25[last])
    indicator_signal[2] = GOLDEN_CROSS_SIGNAL(sma50[last - 1], sma50[last], sma200[last - 1], sma200[last])
    indicator_signal[3] = RSI_SIGNAL(rsi[last])
    indicator_signal[4] = RSI_SIGNAL(stochRSI[last])
    return indicator_signal


def GOLDEN_FIVE_SIGNAL(Golden_Nums):
    if Golden_Nums[0] >= DEF.Golden_Five_Buy_Limit: return 1
    elif Golden_Nums[1] >= DEF.Golden_Five_Sell_Limit: return -1
    return 0
# ----------------------------------------------------------------
