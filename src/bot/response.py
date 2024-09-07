from langchain.prompts import PromptTemplate
from src.core.config_response import Response
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
import os

custom_prompt = """
Use the following pieces of context to answer the question at the end. Please provide
a short single-sentence summary answer only. If you don't know the answer or if it's
not present in given context, don't try to make up an answer, but suggest me a random
unrelated song title I could listen to.
Context: {context}
Question: {question}
Helpful Answer:
"""

def generate_answer(context, question):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        max_retries=2,
        api_key= os.getenv('OPENAI_API_KEY')
    )
    
    structure_llm = llm.with_structured_output(Response)

    def invoke():
        try:
            return structure_llm.invoke(custom_prompt.format(context=context, question=question)) 
        except Exception:
            print("Error")
            return invoke()
    
    return dict(invoke())
    