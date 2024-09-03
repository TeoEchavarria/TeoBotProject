from src.utils.mongodb import collection, insert
from src.embeddings.embedder import get_embedding_from_markdown_url
import pandas as pd

def fetch_collections():
    # Fetch collections from MongoDB
    collections_list = collection("notes")

    # Convert collections to dataframe
    df = pd.DataFrame(collections_list)

    return df

