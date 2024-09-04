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
            lines = content.split('\n')
            title = ''
            for line in lines:
                if line.startswith('# '):
                    title += f'{line[2:]} ' 
                    break
            content = content.replace('#', '').replace("\n", " ").replace("\\", "").replace("[[" , "").replace("]]", "")
            if title == '':
                title = "Untitled" 

            element_id = os.path.splitext(file_name)[0] 
            existing_document = find_one("notes", {"id": element_id})
            if existing_document:
                updated = False
                if existing_document["title"] != title or existing_document["content"] != content:
                    updated = True
                update_data = {
                    "title": title,
                    "content": content,
                    "updated": not updated
                }
                update_one("notes", {"id": element_id}, update_data)  
            else:
                data = {
                    "id": element_id,
                    "title": title,
                    "content": content,
                    "embedding_title": None,
                    "embedding_content": None,
                    "updated": False
                }
                insert("notes", data) 