from src.core.config_response import Response
from src.core.logger import LoggingUtil
from langchain_openai import ChatOpenAI
import os

custom_prompt = """
Context: {context}
Question: {question}
Helpful Answer:
"""

logger = LoggingUtil.setup_logger()


def generate_answer(context, question, openai_key):
    llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=0.8, max_retries=2, api_key=openai_key
    )

    structure_llm = llm.with_structured_output(Response)

    def invoke():
        try:
            logger.info("Generating answer for question")
            return structure_llm.invoke(
                custom_prompt.format(context=context, question=question)
            )
        except Exception as e:
            logger.error("Error generating answer: %s", e)

    return dict(invoke())
