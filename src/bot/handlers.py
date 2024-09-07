from telegram import Update
from telegram.ext import ContextTypes
from src.bot.authentication import authenticate

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu asistente de notas, aquí para ayudarte a organizar tus ideas con la tecnología de Pinecone y OpenAI.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.response_flow import response_flow
    if await authenticate(update):
        answer = await response_flow(update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text = answer["text"])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")
