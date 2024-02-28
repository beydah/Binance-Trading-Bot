# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import algotest as TEST
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


# Signal Calculations
def DCA(OLD_PRICE, PRICE, OLD_SMA25, SMA25):
    if OLD_PRICE < OLD_SMA25 and PRICE > SMA25: return 1
    if OLD_PRICE > OLD_SMA25 and PRICE < SMA25: return -1
    return 0


def GOLDENCROSS(OLD_SMA50, SMA50, OLD_SMA200, SMA200):
    if OLD_SMA50 < OLD_SMA200 and SMA50 > SMA200: return 1
    if OLD_SMA50 > OLD_SMA200 and SMA50 < SMA200: return -1
    return 0


def RSI(RSI_NUM):
    if RSI_NUM < 30: return 1
    if RSI_NUM > 70: return -1
    return 0


def GOLDENFIVE(GOLDEN_NUMS):
    if GOLDEN_NUMS[0] >= 3: return 1
    if GOLDEN_NUMS[1] >= 3: return -1
    return 0


def FIVEPERIOD(COIN_SYMBOL, DATETIME):
    signalBuy = signalSell = 0
    for period in DEF.CANDLE_PEROIDS:
        closePrice = CANDLE.READ(COIN_SYMBOL, period, DATETIME, 250, 4)
        # TODO: Golden Five Indıcator'unu Duzenle Yeni Duzen: GoldenFive(CoinSymbol,ClosePrice)
        sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], COIN_SYMBOL, None, closePrice)
        ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], COIN_SYMBOL, None, closePrice)
        sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], COIN_SYMBOL, None, closePrice)
        sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], COIN_SYMBOL, None, closePrice)
        rsi = INDICATOR.RSI(COIN_SYMBOL, None, closePrice)
        stochRSI = INDICATOR.STOCHRSI(COIN_SYMBOL, None, closePrice)
        stochRSI_K = stochRSI["stochRSI_K"]
        past = len(closePrice) - 3
        last = len(closePrice) - 2
        if not any(LIB.PD.isna([sma25[past], sma50[past], sma200[past], rsi[past], stochRSI_K[past]])):
            goldenNums = INDICATOR.GOLDENFIVE(closePrice[past], closePrice[last], sma25[past], sma25[last],
                                              sma50[past], sma50[last], sma200[past], sma200[last],
                                              ema25[past], ema25[last], rsi[last], stochRSI_K[last])
            signal = GOLDENFIVE(goldenNums)
        else: signal = 0
        if signal == 1: signalBuy += 1
        elif signal == -1: signalSell += 1
    if signalBuy == signalSell: return 0
    if signalBuy >= 2: return 1
    if signalSell >= 2: return -1
    return 0
# ----------------------------------------------------------------
