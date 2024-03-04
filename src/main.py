# ----------------------------------------------------------------
# Added Links
from src.dataops import candle as CANDLE
from src.dataops import list as LIST
from src.dataops import message as MESSAGE
from src.dataops import wallet as WALLET

from src.engine import analysis as ANALYSIS
from src.engine import algorithm as ALGORITHM
from src.engine import calculator as CALCULATE
from src.engine import indicator as INDICATOR
from src.engine import signal as SIGNAL

from src.settings import api as API
from src.settings import library as LIB
from src.settings import settings as DEF
# ----------------------------------------------------------------


# Test Area
def TEST():
    MESSAGE.SEND(".....TEST START.....")
    MESSAGE.START()
    MESSAGE.SEND(".....TEST END.....")


TEST()
# ----------------------------------------------------------------
