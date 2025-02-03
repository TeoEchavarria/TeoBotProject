from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from src.bot.handlers.basic import clear_context, look_context, page
from src.bot.handlers.talk import talk
from src.bot.handlers.pdf import handle_pdf
from src.bot.handlers.documentation import start, credentials
from src.bot.handlers.embeddings import run_markdown_files
from src.bot.handlers.credentials import (
    github_handler,
    mongo_handler,
    pinecone_handler,
    openai_handler,
)
import os


def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # ----- Handlers -----

    ## Basic handlers
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    credentials_handler = CommandHandler("credentials", credentials)
    application.add_handler(credentials_handler)

    page_handler = CommandHandler("page", page)
    application.add_handler(page_handler)

    clean_context_handler = CommandHandler("clear", clear_context)
    application.add_handler(clean_context_handler)

    look_context_handler = CommandHandler("look", look_context)
    application.add_handler(look_context_handler)

    ## Credentials handlers

    github_command_handler = CommandHandler("github", github_handler)
    application.add_handler(github_command_handler)

    mongo_command_handler = CommandHandler("mongo", mongo_handler)
    application.add_handler(mongo_command_handler)

    pinecone_command_handler = CommandHandler("pinecone", pinecone_handler)
    application.add_handler(pinecone_command_handler)

    openai_command_handler = CommandHandler("openai", openai_handler)
    application.add_handler(openai_command_handler)

    # Embeddings handlers

    markdown_handler = CommandHandler("update", run_markdown_files)
    application.add_handler(markdown_handler)

    # PDF handler
    
    pdf_handler = MessageHandler(filters.Document.PDF, handle_pdf)
    application.add_handler(pdf_handler)

    # Talk handler

    talk_handler = MessageHandler(filters=None, callback=talk)
    application.add_handler(talk_handler)

    application.run_polling()
