import openai
import os

# Set up your OpenAI API credentials

def get_embedding(text, openai_key):
    # Create the embedding using the OpenAI API
    openai.api_key = openai_key
    embedding = openai.embeddings.create(input=text, model="text-embedding-3-large")
    return embedding.data[0].embedding