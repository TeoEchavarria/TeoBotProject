import openai
import os
from src.utils.mongodb import find_element

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')
print(f'OpenAI API Key: {openai.api_key}')

def get_embedding_from_markdown(element):
    # Fetch the content from the Markdown URL
    title = element["title"]
    content = element["content"]

    # Create the embedding using the OpenAI API
    embedding_title = openai.embeddings.create(input=title, model="text-embedding-3-small")
    embedding_content = openai.embeddings.create(input=content, model="text-embedding-3-large")

    # Access the embedding vectors
    embedding_vector_title = embedding_title.data[0].embedding
    embedding_vector_content = embedding_content.data[0].embedding

    print(f"Embedding for {title} created successfully, {len(embedding_vector_title)} and {len(embedding_vector_content)}")
    # Return the JSON structure
    return {
        "id": element["id"],
        "title": title,
        "content": content,
        "embedding_title": embedding_vector_title,
        "embedding_content": embedding_vector_content,
        "updated": True
    }