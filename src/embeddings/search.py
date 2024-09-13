from src.embeddings.embedder import get_embedding
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("notescontent")

def search(text):
    text_embedding = get_embedding(text)
    return index.query(
    namespace="ns2",
    vector=text_embedding,
    top_k=2,
    include_metadata=True
)
    