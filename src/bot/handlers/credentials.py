from telegram import Update
from telegram.ext import ContextTypes
from src.document_processing.loader import update_markdown_files
from src.utils.mongodb import add_or_update_key
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

async def pinecone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text('Usage: /pinecone <pinecone_key>')
        return

    pinecone_key = args[0]
    try:
        add_or_update_key(update.message.from_user.username, pinecone_key=pinecone_key)
        await update.message.reply_text("Pinecone key added to user")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error using pinecone handler - Try again")

async def openai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text('Usage: /openai <openai_key>')
        return
    
    openai_key = args[0]
    try:
        add_or_update_key(update.message.from_user.username, openai_key=openai_key)
        await update.message.reply_text("OpenAI key added to user")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error using openai handler - Try again")

async def github_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text('Usage: /github <user_name> <repo> <directory_path>')
        return

    owner, repo, directory_path = args

    try:
        add_or_update_key(update.message.from_user.username, owner=owner, repo=repo, directory_path=directory_path)
        count = await update_markdown_files(context, update, update.message.from_user.username)
        message_text = f"{count} Files extract from {owner}/{repo}/{directory_path}"
        await update.message.reply_text(message_text)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error using github handler - Try again")

async def mongo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text('Usage: /mongo <mongo_key>')
        return

    mongo_key = args[0]
    try:
        collection = add_or_update_key(update.message.from_user.username, mongo_key=mongo_key)
        message_text = f"Mongo key added to user {update.message.from_user.username}"
        await update.message.reply_text(message_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Error using mongodb handler - Try again")
