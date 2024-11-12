from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.document_processing.loader import update_markdown_files
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"

async def run_markdown_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        count = await update_markdown_files(context, update, update.message.from_user.username)
        message_text = f"{count} Files updated"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)
    except Exception as e:
        logger.error(f"Error processing markdown files : {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Error processing markdown files")