from pinecone import Pinecone
import os
from src.utils.mongodb import collection

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("notescontent")

async def upsert_embeddings_to_pinecone():
    pinecone_vectors = [
                {
                    "id": element["id"],
                    "values": element["embedding_content"],
                    "metadata": {
                        "title": element["title"],
                        "content": element["content"]
                    }
                }
            for element in collection("notes")]
    index.upsert(vectors=pinecone_vectors, namespace="ns1")