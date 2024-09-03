from src.document_processing.loader import fetch_collections

if __name__ == "__main__":
    df = fetch_collections()
    print(df.head())