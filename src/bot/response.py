import json
import os
from openai import OpenAI

def generate_answer(context, question, openai_key, mode = "response") -> dict:
    try:
        if openai_key is None:
            client = OpenAI(
                base_url="http://localhost:11434/v1",  # default Ollama port
                api_key="ollama-local"                 # can be any string
            )
        else:
            # Use your OpenAI API key from environment or wherever you store it
            client = OpenAI(api_key=openai_key)
        
        prompt = "" if openai_key is None else "You have a free membership"

        # mode = ["response", "pdf_extract", "note_create"]
        json_format = json.load(open(f'src/bot/functions/{mode}.json'))

        # Call the chat completion
        response = client.chat.completions.create(
            model="deepseek-r1:7b" if openai_key is None else "gpt-4o-2024-08-06",  
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{context} {question}"
                        }
                    ]
                }
            ],
            temperature=0.2,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            response_format=json_format
        )

        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        return {"text": "I'm sorry I couldn't generate an answer for you. Would you like to ask me something else?"}
