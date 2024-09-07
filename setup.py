from src.document_processing.loader import process_markdown_files, process_data_embeddings
from src.embeddings.pinecone import upsert_embeddings_to_pinecone
from src.embeddings.search import search
from src.bot.response import generate_answer
from dotenv import load_dotenv
from src.bot.bot import main

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    #process_markdown_files("/Users/teoechavarria/Documents/GitHub/knowledge-page/content")
    #process_data_embeddings()
    #upsert_embeddings_to_pinecone()
    #print(search("Predicciones con datos a travez del tiempo"))
    #main()
    
    output = generate_answer("The capital of France is Paris.", "What is the capital of France?")
    print(output)