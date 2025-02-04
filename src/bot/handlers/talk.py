from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os

from src.services.voice_to_text import transcribe_voice
from src.bot.response import generate_answer
from src.bot.response_flow import response_flow
from src.utils.mongodb import find_one


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
     # 1. Check if the user sent a voice note or a text message
    user = find_one("users", {"_id": update.message.from_user.username})
    reply_markup = None
    if update.message.voice:
        # It's a voice note
        try:
            user_message_text, time = await transcribe_voice(update, context, user["openai_key"])
            if time == -1:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, you don't have enough time left to send voice messages."
                )
                return
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, I was unable to transcribe your voice memo. Please try again."
            )
            return
    else:
        user_message_text = update.message.text

    try:
        with open(f"context_{update.message.from_user.username}.txt", "r") as file:
            context_content = file.read()
        
        if user_message_text.split(" ")[0].lower().replace(",", "").replace(".", "") in ["search","busca", "buscar"]:
            context_emb, answer = await response_flow(user_message_text, user["openai_key"], user["pinecone_key"], user["mongo_key"])
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
        else:
            answer = generate_answer(
                context_content, user_message_text, user["openai_key"]
            )
        with open(f"context_{update.message.from_user.username}.txt", "a") as file:
            file.write(answer["text"])
    except Exception as e:
        answer = {
            "text": "I'm sorry I couldn't generate an answer for you. Would you like to ask me something else?"
        }
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer["text"], reply_markup=reply_markup, parse_mode="Markdown"
    )
