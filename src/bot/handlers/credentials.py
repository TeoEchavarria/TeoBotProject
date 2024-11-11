from telegram import Update
from telegram.ext import ContextTypes
from src.services.github.github_extract import get_github_directory_files
from src.utils.mongodb import upsert
import os

async def github_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text('Usage: /github <user_name> <repo> <directory_path>')
        return

    owner, repo, directory_path = args
    token = os.getenv("GITHUB_TOKEN")

    try:
        files = get_github_directory_files(owner, repo, directory_path, token)
        search = {
            "_id": update.message.from_user,  # Use username as the unique identifier
            "owner": owner,
            "repo": repo,
            "directory_path": directory_path
        }
        upsert("users", search)
        message_text = f"{len(files)} Files in {directory_path} of {owner}/{repo}"
        await update.message.reply_text(message_text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(str(e))


