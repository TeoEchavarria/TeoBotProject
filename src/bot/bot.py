import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from src.bot.handlers import start, search
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    search_handler = MessageHandler(filters=None, callback=search)
    application.add_handler(search_handler)
    
    application.run_polling()