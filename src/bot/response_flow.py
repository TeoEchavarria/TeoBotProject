from src.services.embeddings.search import search
from src.bot.response import generate_answer
from src.core.logger import LoggingUtil
from src.utils.mongodb import find_one
import os

logger = LoggingUtil.setup_logger()


async def response_flow(question, openai_key, pinecone_key, mongo_key):
    embedding = await search(question, openai_key, pinecone_key)
    embedding = embedding["matches"]
    if len(embedding) == 0:
        return "", {"text": "No matches found"}
    context = [
        {"url": match["metadata"]["url"], "content": find_one("notes", {"_id": match["metadata"]["url"]}, mongo_key)["content"]}
        for match in embedding
    ]
    context_answer = "\n".join(cont["content"] for cont in context)
    answer = generate_answer(
        context_answer, question.replace("/search ", ""), openai_key
    )
    return context, answer
