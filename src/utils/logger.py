import logging
import sys
from pathlib import Path

# region Logger Setup
def F_Setup_Logger(p_name: str = "BinanceBot", p_log_level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger instance.
    """
    logger: logging.Logger = logging.getLogger(p_name)
    logger.setLevel(p_log_level)
    
    if logger.hasHandlers():
        return logger
        
    # Console Handler
    c_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    c_handler.setLevel(p_log_level)
    c_format: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    logger.addHandler(c_handler)
    
    # File Handler
    logs_dir: Path = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    f_handler: logging.FileHandler = logging.FileHandler(logs_dir / "bot.log", encoding='utf-8')
    f_handler.setLevel(p_log_level)
    f_format: logging.Formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    
    return logger
# endregion

LOGGER: logging.Logger = F_Setup_Logger()
