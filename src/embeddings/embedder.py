import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embedding(text):
    # Create the embedding using the OpenAI API
    embedding = openai.embeddings.create(input=text, model="text-embedding-3-large")
    return embedding.data[0].embedding

def get_embedding_from_markdown(element):
    # Fetch the content from the Markdown URL
    url = element["url"]
    content = element["content"]

    # Create the embedding using the OpenAI API
    embedding_content = openai.embeddings.create(input=content, model="text-embedding-3-large")

    # Access the embedding vectors
    embedding_vector_content = embedding_content.data[0].embedding

    # Return the JSON structure
    return {
        "id": element["id"],
        "url": url,
        "content": content,
        "embedding_content": embedding_vector_content,
        "updated": True
    }