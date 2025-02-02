import json
import os
from openai import OpenAI

def generate_answer(context, question, openai_key) -> dict:
        openai_key = None  
        if openai_key is None:
            client = OpenAI(
                base_url="http://localhost:11434/v1",  # default Ollama port
                api_key="ollama-local"                 # can be any string
            )
        else:
            # Use your OpenAI API key from environment or wherever you store it
            client = OpenAI(api_key=openai_key)
        
        prompt = "" if openai_key is None else "You have a free membership"

        json_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The main text content"
                        },
                        "image_url": {
                            "type": "string",
                            "description": "URL of the image. In the case of existing"
                        },
                        "link_url": {
                            "type": "number",
                            "description": "URL of a related link. In the case of existing"
                        },
                    },
                    "required": ["text", "image_url", "link_url"],
                    "additionalProperties": False
                }
            }
        }


        # Call the chat completion
        response = client.chat.completions.create(
            model="deepseek-r1:7b" if openai_key is None else "gpt-4o-mini",  
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