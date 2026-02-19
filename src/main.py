from src.utils.logger import LOGGER
from src.bot import main as BOT

if __name__ == "__main__":
    try:
        LOGGER.info("Starting Application")
        BOT.run()
    except Exception as e:
        LOGGER.critical(f"App Crashed: {e}")
