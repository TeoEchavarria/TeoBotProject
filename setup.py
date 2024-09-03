from src.document_processing.loader import process_markdown_files, process_data_embeddings, update_all_updated
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    process_markdown_files("/Users/teoechavarria/Documents/GitHub/knowledge-page/content")
    process_data_embeddings()