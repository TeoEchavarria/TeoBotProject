from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.bot.authentication import authenticate
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"

async def look_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await authenticate(update):
        with open(f"context_{update.message.from_user.username}.txt", "r") as file:
            context_file = file.read()
        if context_file == "":
            context_file = "No context found"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=context_file)
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
        await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu asistente de notas, aquí para ayudarte a organizar tus ideas con la tecnología de Pinecone y OpenAI.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

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
        keyboard = [
        [InlineKeyboardButton(note["url"].replace("-", " "), url=f"{os.getenv('WEB_NOTES')}{note["url"]}") for note in context_emb]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text = answer["text"], reply_markup=reply_markup)
        
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
        
async def run_markdown_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.document_processing.loader import process_markdown_files
    if await authenticate(update):
        try:
            process_markdown_files(os.getenv("MARKDOWN_NOTES"))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Markdown files processed")
        except Exception:
            logger.error("Error processing markdown files")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error processing markdown files")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)

async def run_pinecone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.document_processing.loader import process_data_embeddings
    if await authenticate(update):
        try:
            process_data_embeddings()
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Pinecone updated")
        except Exception:
            logger.error("Error updating Pinecone")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Error updating Pinecone")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_not_permissions)