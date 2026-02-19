# ----------------------------------------------------------------
import time
import threading
import schedule
import telebot
from src.constants import TELEGRAM_TOKEN
from src.utils.logger import LOGGER
from src.bot import handlers as H
from src.bot import messenger as MSG
from src.services import market_data_service as DATA

# Scheduler Jobs
def job_new_day():
    try:
        LOGGER.info("Executing New Day Protocol")
        MSG.send_message("New Day Protocol Start")
        DATA.calculate_wallet_changes()
        # Display Info? Original bot.py called CALCULATE.F_Wallet_Changes_Info
        # We can implement display logic in handlers or here
        pass
    except Exception as e:
        LOGGER.error(f"New Day Job Error: {e}")

def job_new_hour():
    try:
        LOGGER.info("Executing New Hour Protocol")
        MSG.send_message("New Hour Protocol Start")
        DATA.calculate_coinlist_changes()
        DATA.update_favorites()
    except Exception as e:
        LOGGER.error(f"New Hour Job Error: {e}")

def run_scheduler():
    LOGGER.info("Starting Scheduler Processor...")
    schedule.every().hour.at(":00").do(job_new_hour)
    schedule.every().day.at("00:00").do(job_new_day)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            LOGGER.error(f"Scheduler Error: {e}")
            time.sleep(5)

# Main Bot Entry
def run():
    # Start Scheduler in background
    t = threading.Thread(target=run_scheduler)
    t.daemon = True # Kill when main thread exits
    t.start()
    
    # Start Bot
    if not TELEGRAM_TOKEN:
        LOGGER.critical("Telegram Token not found!")
        return

    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    
    @bot.message_handler(func=lambda m: True)
    def on_message(message):
        try:
            # Check user ID? Original code checked API.Telegram_User_ID
            # We should probably check it here
            from src.constants import TELEGRAM_USER_ID
            if str(message.from_user.id) != TELEGRAM_USER_ID:
                LOGGER.warning(f"Unauthorized access attempt from {message.from_user.id}")
                return
                
            H.handle_message(message.from_user.first_name, message.text)
        except Exception as e:
            LOGGER.error(f"Message Handler Error: {e}")

    LOGGER.info("Starting Telegram Bot Polling...")
    bot.infinity_polling()
