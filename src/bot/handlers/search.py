from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"


async def search_embeddings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.response_flow import response_flow
    from src.utils.mongodb import find_one
    user = find_one("users", {"_id": update.message.from_user.username})
    try:
        context_emb, answer = (
            await response_flow(update.message.text, user["openai_key"], user["pinecone_key"], user["mongo_key"])
            if update.message.text != "/search"
            else ["", {"text": "No matches found"}]
        )
        with open(f"context_{update.message.from_user.username}.txt", "a") as file:
            file.write("\n".join([cont["content"] for cont in context_emb]))
            file.write(answer["text"])
    except Exception as e:
        logger.error(f"Error generating answer with embeddings : {e}")
        answer = {
            "text": "SEARCH: I'm sorry I couldn't generate an answer for you. Would you like to ask me something else?" if user["openai_key"] or  user["pinecone_key"] else "SEARCH: You need to add your OpenAI and Pinecone keys first"
        }
        context_emb = []
    keyboard = [
        [
            InlineKeyboardButton(
                note["url"].replace("-", " ").replace(".md", "").capitalize(),
                url=f"{os.getenv('WEB_NOTES')}{note['url'].replace(' ', '-').replace('.md', '')}",
            )
            for note in context_emb
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer["text"], reply_markup=reply_markup, parse_mode="Markdown"
    )
