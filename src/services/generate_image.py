import os
from pathlib import Path
from google import genai  # type: ignore
from google.genai import types  # type: ignore
from PIL import Image  # type: ignore
from io import BytesIO
import base64

def generate_image(
    prompt: str,
    *,
    model: str = "gemini-2.0-flash-exp-image-generation",
) :
    """Generate an image from *prompt* using Google Gemini.

    Returns the *out_path* where the image was saved.
    """

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Define GOOGLE_API_KEY env var before calling generate_image()")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]           
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            return base64.b64encode(part.inline_data.data).decode('utf-8')
    raise RuntimeError("Gemini did not return an image; refine your prompt or check your quota")