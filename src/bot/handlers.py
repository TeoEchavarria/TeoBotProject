from telegram import Update
from telegram.ext import ContextTypes
from src.bot.authentication import authenticate


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot, please talk to me!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Respuesta del BOT")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")
