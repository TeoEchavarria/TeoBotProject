from src.document_processing.loader import process_markdown_files, process_data_embeddings
from src.utils.mongodb import collection
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    #process_markdown_files("/Users/teoechavarria/Documents/GitHub/knowledge-page/content")
    #process_data_embeddings()
    df = pd.DataFrame(collection("notes"))
    print(df.columns)