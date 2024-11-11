from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.bot.authentication import authenticate
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"

async def run_markdown_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.document_processing.loader import process_markdown_files
    if await authenticate(update):
        try:
            process_markdown_files(os.getenv("MARKDOWN_NOTES"))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Markdown files processed")
        except Exception:
            logger.error("Error processing markdown files")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error processing markdown files")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

async def run_pinecone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.document_processing.loader import process_data_embeddings
    from src.embeddings.pinecone import upsert_embeddings_to_pinecone
    if await authenticate(update):
        try:
            await process_data_embeddings()
            await upsert_embeddings_to_pinecone()
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Pinecone updated")
        except Exception:
            logger.error("Error updating Pinecone")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error updating Pinecone")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)