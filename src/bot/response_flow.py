from src.embeddings.search import search
from src.bot.response import generate_answer
from src.core.logger import LoggingUtil

logger = LoggingUtil.setup_logger()

async def response_flow(question):
    logger.info("Searching for matches")
    embedding = search(question)["matches"]
    logger.info(f"Matches found: {embedding}")
    context = "\n".join([f'TITLE:{match["metadata"]["title"]}={match["metadata"]["content"]}' for match in embedding])
    
    logger.info("Generating answer")
    answer = dict(generate_answer(context, question))
    
    return answer