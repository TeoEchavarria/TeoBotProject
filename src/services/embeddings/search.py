from src.services.embeddings.embedder import get_embedding
from pinecone import Pinecone
import os

async def search(text, openai_key, pinecone_key):
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index("notescontent")
    text_embedding = get_embedding(text, openai_key)
    return index.query(
        namespace="ns1", vector=text_embedding, top_k=2, include_metadata=True
    )
