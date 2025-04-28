import os
from pathlib import Path
from google import genai  # type: ignore
from google.genai import types  # type: ignore
from PIL import Image  # type: ignore
from io import BytesIO

def generate_image(
    prompt: str,
    *,
    out_path: str | Path = "gemini_image.png",
    model: str = "imagen-3.0-generate-002",
    aspect_ratio: str | None = None,
) -> Path:
    """Generate an image from *prompt* using Google Gemini.

    Returns the *out_path* where the image was saved.
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Define GOOGLE_API_KEY env var before calling generate_image()")

    client = genai.Client(api_key=api_key)

    cfg = {
        "response_modalities": ["IMAGE"],
    }
    if aspect_ratio:
        cfg["aspect_ratio"] = aspect_ratio

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=types.GenerateContentConfig(**cfg),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data:
            img = Image.open(BytesIO(part.inline_data.data))
            img.save(out_path)
            return Path(out_path)
    raise RuntimeError("Gemini did not return an image; refine your prompt or check your quota")
