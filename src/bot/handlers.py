from telegram import Update
from telegram.ext import ContextTypes
from src.bot.authentication import authenticate
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

async def look_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        with open(f"context_{update.message.from_user.username}.txt", "r") as file:
            context_file = file.read()
        if context_file == "":
            context_file = "No context found"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=context_file)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

async def clear_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        with open(f"context_{update.message.from_user.username}.txt", "w") as file:
            file.write("")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Context cleared")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        file_path = f"context_{ update.message.from_user.username}.txt"
        open(file_path, "w").close()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu asistente de notas, aquí para ayudarte a organizar tus ideas con la tecnología de Pinecone y OpenAI.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

async def search_embeddings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.response_flow import response_flow
    if await authenticate(update):
        try:
            context_emb , answer = await response_flow(update.message.text) if update.message.text != "/search" else ["", {"text": "No matches found"}]
            with open(f"context_{update.message.from_user.username}.txt", "a") as file:
                file.write(context_emb)
                file.write(answer["text"])
        except Exception:
            logger.error("Error generating answer with embeddings")
            answer = {"text": "SEARCH: I'm sorry I couldn't generate an answer for you. Would you like to ask me something else?"}
        await context.bot.send_message(chat_id=update.effective_chat.id, text = answer["text"])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")

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
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this bot")