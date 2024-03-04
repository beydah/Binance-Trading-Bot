# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import algorithm as ALGORITHM
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL
from src.engine import analysis as ANALYSIS

from src.settings import settings as DEF
from src.settings import library as LIB
from src.settings import api as API
# ----------------------------------------------------------------


def COINLIST_INFO():
    LIST.WRITE_CHANGE()
    df = LIST.READ_CHANGE()
    maxAVGList = LIB.HEAP.nlargest(5, df["AVG_Percent"])
    maxCoinList = df.loc[df["AVG_Percent"].isin(maxAVGList), ["Coin_Symbol", "AVG_Percent"]]
    minAVGList = LIB.HEAP.nsmallest(5, df["AVG_Percent"])
    minCoinList = df.loc[df["AVG_Percent"].isin(minAVGList), ["Coin_Symbol", "AVG_Percent"]]
    MESSAGE.SEND(f"Alert List: \n{maxCoinList}")
    MESSAGE.SEND(f"Favorite List: \n{minCoinList}")


def WALLET_INFO():
    fullTotalWallet = CALCULATE.TOTAL_WALLET()
    spotTotalWallet = CALCULATE.TOTAL_WALLET(0)
    earnTotalWallet = CALCULATE.TOTAL_WALLET(1)
    message = (f"Total Wallet {fullTotalWallet}\n"
               f"Spot Total Wallet {spotTotalWallet}\n"
               f"Earn Total Wallet {earnTotalWallet}\n")
    MESSAGE.SEND(message)
    changeInfo = WALLET.READ_TOTAL_BALANCE()
    changeInfo = changeInfo.transpose()
    changeInfo = changeInfo.to_string()
    message = f"Changes Info\n{changeInfo}\n"
    MESSAGE.SEND(message)


def COIN_INFO(COIN):
    found = CALCULATE.FIND_COIN(COIN)
    if not found: return
    if COIN == "USDT":
        MESSAGE.SEND("USDT is not available for use.")
        return
    coinSymbol = COIN + "USDT"
    closePrice = CANDLE.READ(coinSymbol, "30m", CANDLE_LIMIT=205, HEAD_ID=4)
    sma25 = INDICATOR.SMA(DEF.MA_LENGTHS[0], CLOSE_PRICE=closePrice)
    ema25 = INDICATOR.EMA(DEF.MA_LENGTHS[0], CLOSE_PRICE=closePrice)
    sma50 = INDICATOR.SMA(DEF.MA_LENGTHS[1], CLOSE_PRICE=closePrice)
    sma200 = INDICATOR.SMA(DEF.MA_LENGTHS[2], CLOSE_PRICE=closePrice)
    rsi = INDICATOR.RSI(CLOSE_PRICE=closePrice)
    stochRSI = INDICATOR.STOCHRSI(CLOSE_PRICE=closePrice)
    stochRSI_K = stochRSI["stochRSI_K"]
    old = len(closePrice) - 3
    last = len(closePrice) - 2
    signals = ["None", "None", "None", "None", "None"]
    if not any(LIB.PD.isna([stochRSI_K[old], rsi[old], sma200[old], sma50[old], sma25[old]])):
        smaSignal = SIGNAL.DCA(closePrice[old], closePrice[last], sma25[old], sma25[last])
        if smaSignal == 1: signals[0] = "BUY"
        elif smaSignal == -1: signals[0] = "SELL"
        emaSignal = SIGNAL.DCA(closePrice[old], closePrice[last], ema25[old], ema25[last])
        if emaSignal == 1: signals[1] = "BUY"
        elif emaSignal == -1: signals[1] = "SELL"
        goldenCrossSignal = SIGNAL.GOLDENCROSS(sma50[old], sma50[last], sma200[old], sma200[last])
        if goldenCrossSignal == 1: signals[2] = "BUY"
        elif goldenCrossSignal == -1: signals[2] = "SELL"
        rsiSignal = SIGNAL.RSI(rsi[last])
        if rsiSignal == 1: signals[3] = "BUY"
        elif rsiSignal == -1: signals[3] = "SELL"
        stochRSISignal = SIGNAL.RSI(stochRSI_K[last])
        if stochRSISignal == 1: signals[4] = "BUY"
        elif stochRSISignal == -1: signals[4] = "SELL"
    MESSAGE.SEND(f"Coin: {COIN}\nPrice: {float(closePrice[len(closePrice)-1])}\n"
                 f"SMA: {signals[0]}\nEMA: {signals[1]}\n"
                 f"Golden Cross: {signals[2]}\nRSI: {signals[3]}\n"
                 f"StochRSI: {signals[4]}\n")
