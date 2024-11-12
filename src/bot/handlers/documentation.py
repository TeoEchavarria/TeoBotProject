from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.core.logger import LoggingUtil
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_path = f"context_{update.message.from_user.username}.txt"
    open(file_path, "w").close()  # Asegúrate de entender por qué haces esto. Parece redundante si solo quieres leer de otro archivo.
    
    # Asumiendo que la variable de entorno 'START_MESSAGE_FILE' contiene la ruta al archivo Markdown.
    with open(os.getenv("START_MESSAGE_FILE"), "r", encoding="utf-8") as file:
        start_message = file.read()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message,
        parse_mode='Markdown'  # Asegúrate de que el texto del archivo .md sea compatible con Markdown.
    )

async def credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("./src/documents/credentials.md", "r", encoding="utf-8") as file:
        start_message = file.read()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message,
        parse_mode='Markdown'  # Asegúrate de que el texto del archivo .md sea compatible con Markdown.
    )