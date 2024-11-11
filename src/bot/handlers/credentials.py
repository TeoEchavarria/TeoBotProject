from telegram import Update
from telegram.ext import ContextTypes
from src.services.github.github_extract import get_github_directory_files
from src.utils.mongodb import upsert
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

def add_or_update_key(username, mongo_key=None, owner=None, repo=None, directory_path=None):
    search = {
        "_id": username
    }
    update_data = {
        "mongo_key": mongo_key,
        "owner": owner,
        "repo": repo,
        "directory_path": directory_path
    }
    # Remove any None values, only update provided values
    update_data = {k: v for k, v in update_data.items() if v is not None}

    result = upsert("users", search, update_data)
    return True

async def github_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text('Usage: /github <user_name> <repo> <directory_path>')
        return

    owner, repo, directory_path = args

    try:
        files = get_github_directory_files(owner, repo, directory_path)
        add_or_update_key(update.message.from_user.username, owner=owner, repo=repo, directory_path=directory_path)
        message_text = f"{len(files)} Files in {directory_path} of {owner}/{repo}"
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
