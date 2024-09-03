from src.document_processing.loader import process_markdown_files
from src.utils.mongodb import collection
from dotenv import load_dotenv



if __name__ == "__main__":
    load_dotenv()
    process_markdown_files("/Users/teoechavarria/Documents/GitHub/knowledge-page/content")
    print(collection("notes"))