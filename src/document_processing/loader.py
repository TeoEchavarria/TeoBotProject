import os
from src.utils.mongodb import insert, find_one, update_one, collection
from src.embeddings.embedder import get_embedding_from_markdown

def process_data_embeddings():
    for element in collection("notes"):
        if not element["updated"]:
            update_one("notes", {"id": element["id"]}, get_embedding_from_markdown(element))  


def process_markdown_files(folder_path):
    markdown_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    print(f"Found {len(markdown_files)} markdown files in {folder_path}")
    for file_name in markdown_files:
        print(f"Processing {file_name}")
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            url = file_path.split("/")[-1].replace(".md", "").replace(" ", "-")
            content = content.replace('#', '').replace("\n", " ").replace("\\", "").replace("[[" , "").replace("]]", "")

            existing_document = find_one("notes", {"url": url})
            print(f"Existing document: {existing_document}")
            if existing_document:
                updated = False
                if existing_document["url"] != url or existing_document["content"] != content:
                    updated = True
                update_data = {
                    "url": url,
                    "content": content,
                    "updated": not updated
                }
                update_one("notes", {"url": url}, update_data)  
            else:
                data = {
                    "url": url,
                    "content": content,
                    "embedding_content": None,
                    "updated": False
                }
                print(data)
                insert("notes", data) 