from telegram import Update
from telegram.ext import ContextTypes
from src.document_processing.loader import update_markdown_files
from src.utils.mongodb import find_one
from src.services.embeddings.pinecone import upsert_embeddings_to_pinecone
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"


async def run_markdown_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = await update_markdown_files(
            context, update, update.message.from_user.username
        )
        message_text = f"{count} Files updated"
        user = find_one("users", {"_id": update.message.from_user.username})
        await upsert_embeddings_to_pinecone(user["pinecone_key"], user["mongo_key"])
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=message_text
        )
    except Exception as e:
        logger.error(f"Error processing markdown files : {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Error processing markdown files"
        )
