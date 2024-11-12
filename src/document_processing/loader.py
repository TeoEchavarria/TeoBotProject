import os
import requests
from src.utils.mongodb import insert, find_one, update_one, collection
from src.services.embeddings.embedder import get_embedding
from src.services.github.github_extract import get_github_directory_files
from src.core.logger import LoggingUtil

logger = LoggingUtil.setup_logger()

async def update_text(context, update, count):
    if count == 1:
        message = await update.message.reply_text('1 File updated')
        context.user_data['message_id'] = message.message_id
        if context.user_data.get('message_id') is None:
            context.user_data['message_id'] = message.id
    else:
        chat_id = update.effective_chat.id
        message_id = context.user_data.get('message_id')
        message_text = f"{count} Files updated"
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message_text)

def download_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download file from {url}")

async def update_markdown_files(context, update, user_name, files = None):
    from src.utils.mongodb import find_one, create_db_and_collection
    user = find_one("users", {"_id": user_name})
    if user is None:
        return "User not found"
    try:
        create_db_and_collection(user["mongo_key"], "Notes_bot", "notes")
        if not files:
            files = get_github_directory_files(user["owner"], user["repo"], user["directory_path"])
        count = await process_markdown_files(context, update, user["openai_key"], files)
        return count
    except Exception as e:
        logger.error(f"Error updating markdown files: {e}")
        raise Exception("Error updating markdown files")

async def process_markdown_files(context, update, openai_key , files,mongo_key = None):
    count = 0
    for file_name, url_content in files.items():
        content = download_file_content(url_content)
        content = content.replace('#', '').replace("\n", " ").replace("\\", "").replace("[[" , "").replace("]]", "")
        existing_document = find_one("notes", {"_id": file_name}, mongo_key)
        if existing_document:
            updated = False
            if existing_document["_id"] != file_name or existing_document["content"] != content:
                updated = True
                embedding = get_embedding(content, openai_key)
                update_data = {
                    "_id": file_name,
                    "content": content,
                    "updated": not updated,
                    "embedding_content": embedding
                }
                update_one("notes", {"_id": file_name}, update_data)  
                count += 1
                await update_text(context, update, count)
        else:
            embedding = get_embedding(content, openai_key)
            data = {
                "_id": file_name,
                "content": content,
                "embedding_content": embedding,
                "updated": False
            }
            insert("notes", data) 
            count += 1
            await update_text(context, update, count)
        return count
        