from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from src.bot.handlers import start, talk, search_embeddings, clear_context, look_context, run_markdown_files
import os

def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    search_handler = CommandHandler('search', search_embeddings)
    application.add_handler(search_handler)
    
    clean_context_handler = CommandHandler('clear', clear_context)
    application.add_handler(clean_context_handler)
    
    look_context_handler = CommandHandler('look', look_context)
    application.add_handler(look_context_handler)
    
    markdown_files = CommandHandler('runmark', run_markdown_files)
    application.add_handler(markdown_files)
    
    search_handler = MessageHandler(filters=None, callback=talk)
    application.add_handler(search_handler)
    
    application.run_polling()