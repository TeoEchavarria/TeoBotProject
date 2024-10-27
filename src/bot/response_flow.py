from src.services.embeddings.search import search
from src.bot.response import generate_answer
from src.core.logger import LoggingUtil
import os

logger = LoggingUtil.setup_logger()

async def response_flow(question):
    logger.info("Searching for matches")
    embedding = search(question)["matches"]
    if len(embedding) == 0:
        return "", {"text": "No matches found"}
    context = [{"url": match["metadata"]["url"], "content" : match["metadata"]["content"]} for match in embedding]
    context_answer = "\n".join(cont["content"] for cont in context)
    answer = generate_answer(context_answer, question.replace("/search ", ""))
    return context, answer