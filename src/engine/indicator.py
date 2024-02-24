# ----------------------------------------------------------------
# Added Links
from src.engine import dataops as DATA
from src.settings import library as LIB
from src.settings import settings as DEF
# ----------------------------------------------------------------


# Indicator Calculations
def SMA(COIN_SYMBOL, CANDLE_PERIOD, MA_LENGTH, DATETIME=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, None, 4)
        DATA.DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    sma = LIB.TA.ma("sma", CLOSE_PRICE, length=MA_LENGTH)
    return sma


def EMA(COIN_SYMBOL, CANDLE_PERIOD, MA_LENGTH, DATETIME=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, None, 4)
        DATA.DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    ema = LIB.TA.ema(name="ema", close=CLOSE_PRICE, length=MA_LENGTH)
    return ema


def RSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, None, 4)
        DATA.DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    rsi = LIB.TA.rsi(CLOSE_PRICE, DEF.RSI_LENGTH)
    return rsi


def STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME=None, CLOSE_PRICE=None):
    if CLOSE_PRICE is None:
        CLOSE_PRICE = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, None, 4)
        DATA.DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    stochRSI = LIB.TA.stochrsi(CLOSE_PRICE, DEF.STOCHRSI_STOCH_LENGTH, DEF.STOCHRSI_RSI_LENGTH,
                               DEF.STOCHRSI_SMOOTH_K, DEF.STOCHRSI_SMOOTH_D)
    stochRSI.columns = ["stochRSI_K", "stochRSI_D"]
    return stochRSI
# ----------------------------------------------------------------


# Signal Calculations
def DCA_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25):
    if OLD_PRICE < OLD_SMA25 and PRICE > SMA25: return 1
    elif OLD_PRICE > OLD_SMA25 and PRICE < SMA25: return -1
    return 0


def GOLDENCROSS_SIGNAL(OLD_SMA50, SMA50, OLD_SMA200, SMA200):
    if OLD_SMA50 < OLD_SMA200 and SMA50 > SMA200: return 1
    elif OLD_SMA50 > OLD_SMA200 and SMA50 < SMA200: return -1
    return 0


def RSI_SIGNAL(RSI_NUM):
    if RSI_NUM < 30: return 1
    elif RSI_NUM > 70: return -1
    return 0


def MIX_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25, OLD_SMA50, SMA50,
               OLD_SMA200, SMA200, OLD_EMA25, EMA25, RSI_NUM, STOCHRSI_NUM):
    signalBuy = signalSell = 0
    signalLimit = 3
    dcaSignal = DCA_SIGNAL(OLD_PRICE, PRICE, OLD_SMA25, SMA25)
    emaSignal = DCA_SIGNAL(OLD_PRICE, PRICE, OLD_EMA25, EMA25)
    goldenCrossSignal = GOLDENCROSS_SIGNAL(OLD_SMA50, SMA50, OLD_SMA200, SMA200)
    rsiSignal = RSI_SIGNAL(RSI_NUM)
    stochRSISignal = RSI_SIGNAL(STOCHRSI_NUM)
    if dcaSignal == 1: signalBuy += 1
    elif dcaSignal == -1: signalSell += 1
    if emaSignal == 1: signalBuy += 1
    elif emaSignal == -1: signalSell += 1
    if goldenCrossSignal == 1: signalBuy += 1
    elif goldenCrossSignal == -1: signalSell += 1
    if rsiSignal == 1: signalBuy += 1
    elif rsiSignal == -1: signalSell += 1
    if stochRSISignal == 1: signalBuy += 1
    elif stochRSISignal == -1: signalSell += 1
    if signalBuy >= signalLimit: return 1
    elif signalSell >= signalLimit: return -1
    return 0


def MIX_PERIOD_SIGNAL(COIN_SYMBOL, CANDLE_PERIOD, DATETIME):
    closePrice = DATA.READ_CANDLE(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, 250, 4)
    DATA.DELETE_CANDLE(COIN_SYMBOL, CANDLE_PERIOD)
    sma25 = SMA(COIN_SYMBOL, CANDLE_PERIOD, DEF.MA_LENGTHS[0], DATETIME, closePrice)
    ema25 = EMA(COIN_SYMBOL, CANDLE_PERIOD, DEF.MA_LENGTHS[0], DATETIME, closePrice)
    sma50 = SMA(COIN_SYMBOL, CANDLE_PERIOD, DEF.MA_LENGTHS[1], DATETIME, closePrice)
    sma200 = SMA(COIN_SYMBOL, CANDLE_PERIOD, DEF.MA_LENGTHS[2], DATETIME, closePrice)
    rsi = RSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, closePrice)
    stochRSI = STOCHRSI(COIN_SYMBOL, CANDLE_PERIOD, DATETIME, closePrice)
    stochRSI_K = stochRSI["stochRSI_K"]
    past = len(closePrice) - 3
    last = len(closePrice) - 2
    if not any(LIB.PD.isna([stochRSI_K[past], rsi[past], sma50[past], sma25[past]])):
        return MIX_SIGNAL(closePrice[past], closePrice[last], sma25[past], sma25[last],
                          sma50[past], sma50[last], sma200[past], sma200[last], ema25[past],
                          ema25[last], rsi[last], stochRSI_K[last])
    return 0


def PERIOD_SIGNAL(COIN_SYMBOL, DATETIME):
    signalBuy = signalSell = 0
    signalLimit = 2
    for period in DEF.CANDLE_PEROIDS:
        signal = MIX_PERIOD_SIGNAL(COIN_SYMBOL, period, DATETIME)
        if signal == 1: signalBuy += 1
        elif signal == -1: signalSell += 1
    if signalBuy == signalSell: return 0
    if signalBuy >= signalLimit: return 1
    elif signalSell >= signalLimit: return -1
    return 0
# ----------------------------------------------------------------
