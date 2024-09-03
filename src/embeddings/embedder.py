import openai
import os
from src.utils.mongodb import find_element

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embedding_from_markdown_url(element_id):
    # Fetch the content from the Markdown URL
    response = find_element(element_id)
    title = response["title"]
    content = response["content"]

    # Create the embedding using the OpenAI API
    embedding_title = openai.embeddings.create(title, model="text-embedding-3-small")
    embedding_content = openai.embeddings.create(content, model="text-embedding-3-large")

    # Access the embedding vectors
    embedding_vector_title = embedding_title.data[0].embedding
    embedding_vector_content = embedding_content.data[0].embedding

    # Return the JSON structure
    return {
        "id": element_id,
        "title": title,
        "content": content,
        "embedding_title": embedding_vector_title,
        "embedding_content": embedding_vector_content
    }