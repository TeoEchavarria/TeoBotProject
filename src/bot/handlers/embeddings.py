from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.document_processing.loader import update_markdown_files
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"

async def run_markdown_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        files = update_markdown_files(update.message.from_user.username)
        message_text = f"{len(files)} Files updated"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    except Exception:
        logger.error("Error processing markdown files")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error processing markdown files")

async def run_pinecone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.document_processing.loader import process_data_embeddings
    from src.services.embeddings.pinecone import upsert_embeddings_to_pinecone
    try:
        await process_data_embeddings()
        await upsert_embeddings_to_pinecone()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Pinecone updated")
    except Exception:
        logger.error("Error updating Pinecone")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error updating Pinecone")