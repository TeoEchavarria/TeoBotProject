from pinecone import Pinecone
from src.core.logger import LoggingUtil
from future_use.services.mongodb import collection, find_one

logger = LoggingUtil.setup_logger()

async def upsert_embeddings_to_pinecone(pinecone_key, mongo_key):
    try:
        pc = Pinecone(api_key=pinecone_key)
        index = pc.Index("notescontent")
        pinecone_vectors = [
            {
                "id": element["_id"].encode('ascii', 'ignore').decode('ascii'),
                "values": element["embedding_content"],
                "metadata": {"url": element["_id"]}
            }
            for element in collection("notes", mongo_key)
        ]
        index.upsert(vectors=pinecone_vectors, namespace="ns1")
    except Exception as e: 
        logger.error(f"Error upserting embeddings to Pinecone: {e}")
        raise Exception("Error upserting embeddings to Pinecone")
