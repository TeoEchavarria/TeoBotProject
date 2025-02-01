from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.core.logger import LoggingUtil
from src.services.voice_to_text import transcribe_voice
import os

logger = LoggingUtil.setup_logger()

message_not_permissions = "You are not authorized to use this bot"


async def search_embeddings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.response_flow import response_flow
    from src.bot.handlers.basic import clear_context
    from src.utils.mongodb import find_one
    user = find_one("users", {"_id": update.message.from_user.username})
    await clear_context(update, context, True)

    # 1. Check if the user sent a voice note or a text message
    if update.message.voice:
        # It's a voice note
        try:
            user_message_text, time = await transcribe_voice(update, context)
            if time == -1:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, you don't have enough time left to send voice messages."
                )
                return
        except Exception as e:
            logger.error("Error transcribing voice message: %s", e)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, I was unable to transcribe your voice memo. Please try again."
            )
            return
    else:
        user_message_text = update.message.text


    try:
        context_emb, answer = (
            await response_flow(user_message_text, user["openai_key"], user["pinecone_key"], user["mongo_key"])
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
