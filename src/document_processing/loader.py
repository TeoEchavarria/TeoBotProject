import os
import requests
from src.utils.mongodb import insert, find_one, update_one, collection
from src.services.embeddings.embedder import get_embedding_from_markdown
from src.services.github.github_extract import get_github_directory_files

def download_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download file from {url}")

def update_markdown_files(user_name, files = None):
    from src.utils.mongodb import find_one, upsert, create_db_and_collection
    user = find_one("users", {"_id": user_name})
    if user is None:
        return "User not found"
    try:
        create_db_and_collection(user["mongo_key"], "Notes_bot", "notes")
        if not files:
            files = get_github_directory_files(user["owner"], user["repo"], user["directory_path"])
        process_markdown_files(files)
        return files
    except Exception as e:
        return "Error updating markdown files"

def process_markdown_files(files, mongo_key = None):
    for file_name, url_content in files.items():
        content = download_file_content(url_content)
        content = content.replace('#', '').replace("\n", " ").replace("\\", "").replace("[[" , "").replace("]]", "")
        existing_document = find_one("notes", {"_id": file_name}, mongo_key)
        if existing_document:
            updated = False
            if existing_document["url"] != file_name or existing_document["content"] != content:
                updated = True
            update_data = {
                "_id": file_name,
                "content": content,
                "updated": not updated
            }
            update_one("notes", {"_id": file_name}, update_data)  
        else:
            data = {
                "_id": file_name,
                "content": content,
                "embedding_content": None,
                "updated": False
            }
            insert("notes", data) 