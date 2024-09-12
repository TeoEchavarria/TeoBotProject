from pinecone import Pinecone
import os
from src.utils.mongodb import collection

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("notescontent")

async def upsert_embeddings_to_pinecone():
    pinecone_vectors = [
                {
                    "id": element["url"],
                    "values": element["embedding_content"],
                    "metadata": {
                        "url": element["url"],
                        "content": element["content"]
                    }
                }
            for element in collection("notes")]
    index.upsert(vectors=pinecone_vectors, namespace="ns1")