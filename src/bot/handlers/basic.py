from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.bot.authentication import authenticate
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"

async def page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        keyboard = [
        [InlineKeyboardButton("Notes", "https://teoechavarria.github.io/knowledge/notes")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

async def look_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        try:
            with open(f"context_{update.message.from_user.username}.txt", "r") as file:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
        except Exception:
            logger.error("Error sending context")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Context Empty")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

async def clear_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        with open(f"context_{update.message.from_user.username}.txt", "w") as file:
            file.write("")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Context cleared")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        file_path = f"context_{ update.message.from_user.username}.txt"
        open(file_path, "w").close()
        start_message = open(os.getenv("START_MESSAGE_FILE")).read()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.response import generate_answer
    if await authenticate(update):
        try:
            answer = generate_answer(os.getenv("CONTEXT"), update.message.text)
            with open(f"context_{update.message.from_user.username}.txt", "a") as file:
                file.write(answer["text"])
        except Exception:
            logger.error("Error generating answer")
            answer = {"text": "I'm sorry I couldn't generate an answer for you. Would you like to ask me something else?"}
        await context.bot.send_message(chat_id=update.effective_chat.id, text = answer["text"])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)
        