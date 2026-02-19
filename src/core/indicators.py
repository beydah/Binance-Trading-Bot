# ----------------------------------------------------------------
import pandas_ta as ta
from src.constants import MA_LENGTHS, RSI_LENGTHS, GOLDEN_FIVE_BUY_LIMIT, GOLDEN_FIVE_SELL_LIMIT

def F_Sma(p_ma_length: int, p_prices: list): return ta.sma(p_prices, length=p_ma_length)

def F_Ema(p_ma_length: int, p_prices: list): return ta.ema(close=p_prices, length=p_ma_length)

def F_Rsi(p_prices: list): return ta.rsi(p_prices, RSI_LENGTHS[1])

def F_Stoch_Rsi(p_prices: list):
    stochRSI = ta.stochrsi(p_prices, RSI_LENGTHS[0], RSI_LENGTHS[0], RSI_LENGTHS[0], RSI_LENGTHS[0])
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI["stochRSI_K"]

def F_Golden_Five(p_prices: list):
    full_signals = F_Full_Signals(p_prices)
    signal_buy = signal_sell = 0
    for signal in full_signals:
        if signal == 1: signal_buy += 1
        elif signal == -1: signal_sell += 1
    return [signal_buy, signal_sell]

def F_Golden_Five_Test(p_old_price, p_price, p_old_ema25, p_ema25, p_old_sma25, p_sma25,
                     p_old_sma50, p_sma50, p_old_sma200, p_sma200, p_rsi_num, p_stoch_rsi_num):
    ema_signal = F_Dca_Signal(p_old_price, p_price, p_old_ema25, p_ema25)
    dca_signal = F_Dca_Signal(p_old_price, p_price, p_old_sma25, p_sma25)
    golden_cross_signal = F_Golden_Cross_Signal(p_old_sma50, p_sma50, p_old_sma200, p_sma200)
    rsi_signal = F_Rsi_Signal(p_rsi_num)
    stoch_rsi_signal = F_Rsi_Signal(p_stoch_rsi_num)
    indicator_signals = [ema_signal, dca_signal, golden_cross_signal, rsi_signal, stoch_rsi_signal]
    signal_buy = signal_sell = 0
    for signal in indicator_signals:
        if signal == 1: signal_buy += 1
        elif signal == -1: signal_sell += 1
    return [signal_buy, signal_sell]

def F_Dca_Signal(p_old_prices, p_prices, p_old_sma25, p_sma25):
    if p_prices > p_sma25: return 1
    elif p_prices < p_sma25: return -1
    return 0

def F_Golden_Cross_Signal(p_old_sma50, p_sma50, p_old_sma200, p_sma200):
    if p_sma50 > p_sma200: return 1
    elif p_sma50 < p_sma200: return -1
    return 0

def F_Rsi_Signal(p_rsi_num: float):
    if p_rsi_num < 30: return 1
    elif p_rsi_num > 70: return -1
    return 0

def F_Full_Signals(p_prices: list):
    ema25 = F_Ema(p_ma_length=MA_LENGTHS[0], p_prices=p_prices)
    sma25 = F_Sma(p_ma_length=MA_LENGTHS[1], p_prices=p_prices)
    sma50 = F_Sma(p_ma_length=MA_LENGTHS[2], p_prices=p_prices)
    sma200 = F_Sma(p_ma_length=MA_LENGTHS[3], p_prices=p_prices)
    rsi = F_Rsi(p_prices)
    stochRSI = F_Stoch_Rsi(p_prices)
    last = len(p_prices) - 2
    indicator_signal = [0] * 5
    indicator_signal[0] = F_Dca_Signal(p_prices[last - 1], p_prices[last], ema25[last - 1], ema25[last])
    indicator_signal[1] = F_Dca_Signal(p_prices[last - 1], p_prices[last], sma25[last - 1], sma25[last])
    indicator_signal[2] = F_Golden_Cross_Signal(sma50[last - 1], sma50[last], sma200[last - 1], sma200[last])
    indicator_signal[3] = F_Rsi_Signal(rsi[last])
    indicator_signal[4] = F_Rsi_Signal(stochRSI[last])
    return indicator_signal

def F_Golden_Five_Signal(p_golden_nums: list):
    if p_golden_nums[0] >= GOLDEN_FIVE_BUY_LIMIT: return 1
    elif p_golden_nums[1] >= GOLDEN_FIVE_SELL_LIMIT: return -1
    return 0
