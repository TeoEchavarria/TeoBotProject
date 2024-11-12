import openai
import os

# Set up your OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embedding(text):
    # Create the embedding using the OpenAI API
    embedding = openai.embeddings.create(input=text, model="text-embedding-3-large")
    return embedding.data[0].embedding