from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from src.bot.handlers.basic import start, talk, clear_context, look_context, page
from src.bot.handlers.embeddings import run_markdown_files, run_pinecone
from src.bot.handlers.search import search_embeddings
import os

def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    page_handler = CommandHandler('page', page)
    application.add_handler(page_handler)
    
    search_handler = CommandHandler('search', search_embeddings)
    application.add_handler(search_handler)
    
    clean_context_handler = CommandHandler('clear', clear_context)
    application.add_handler(clean_context_handler)
    
    look_context_handler = CommandHandler('look', look_context)
    application.add_handler(look_context_handler)
    
    markdown_handler = CommandHandler('runmark', run_markdown_files)
    application.add_handler(markdown_handler)
    
    pinecone_handler = CommandHandler('runpine', run_pinecone)
    application.add_handler(pinecone_handler)
    
    talk_handler = MessageHandler(filters=None, callback=talk)
    application.add_handler(talk_handler)
    
    application.run_polling()