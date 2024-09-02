import openai
import os
from src.utils.mongodb import find_element

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embedding_from_markdown_url(element_id):
    # Fetch the content from the Markdown URL
    response = find_element(element_id)
    content = response["content"]

    # Create the embedding using the OpenAI API
    embedding = openai.Embed.create(content)

    # Access the embedding vector
    embedding_vector = embedding['embedding']

    return embedding_vector