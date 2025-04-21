import os
import re
import json
import logging
from typing import List, Dict, Any
from typing_extensions import Literal
from pydantic import BaseModel, create_model
from openai import OpenAI

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Initialize OpenAI Client ─────────────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Pydantic models for Step 1 ────────────────────────────────────────────────
class SuggestionOption(BaseModel):
    title: str
    description: str
    type: Literal["string", "number", "integer", "boolean", "object", "array"]

class SuggestionResponse(BaseModel):
    options: List[SuggestionOption]

# ─── Helpers ───────────────────────────────────────────────────────────────────
def normalize_key(title: str) -> str:
    """Convert a human title into snake_case without accents."""
    s = (title.lower()
         .replace("á","a").replace("é","e")
         .replace("í","i").replace("ó","o")
         .replace("ú","u").replace("ñ","n"))
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")

def build_dynamic_model_class(options: List[SuggestionOption]) -> type[BaseModel]:
    """
    Create a Pydantic model where each normalized 'option.title' is a required str field.
    """
    fields = {}
    for opt in options:
        key = normalize_key(opt.title)
        # Each field is a string containing the "generated presentation"
        fields[key] = (str, ...)
    return create_model("PresentationResponse", __base__=BaseModel, **fields)

# ─── Main two‑step function ────────────────────────────────────────────────────
def answer_with_parsed_json(question: str) -> Dict[str, Any]:
    logger.info("Question: %s", question )

    # --- Step 1: Suggest presentation formats, parsed as JSON --------------
    resp1 = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content":
                "Design an optimal answer framework by listing the steps (mechanisms) you’d follow to respond to a complex question for a highly novice audience who knows nothing about the subject but is curious and wants to learn through metaphors, examples, and analogies. Your response must be “chewed up”—very simple—and each step must include at least one concrete example and one metaphor or analogy. For each step, include: 1. The mechanism name. 2. Its purpose. A brief justification. What kind of content such a mechanism should return."
            },
            {"role": "user", "content": question}
        ],
        response_format=SuggestionResponse
    )
    suggestions: SuggestionResponse = resp1.choices[0].message.parsed
    opts = suggestions.options
    logger.info("Received %d options", len(opts))

    # --- Build dynamic Pydantic model from those options ------------------
    PresentationModel = build_dynamic_model_class(opts)

    # --- Step 2: Force JSON response matching dynamic model ---------------
    resp2 = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content":
                "Response in a smooth, short, bold and expert manner. Only return the most valuable and relevant information."
            },
            {"role": "user", "content": question + "\n".join([opt.model_dump()["description"] for opt in opts])}
        ],
        response_format=PresentationModel
    )
    presentation: PresentationModel = resp2.choices[0].message.parsed

    # --- Consolidate result -----------------------------------------------
    return {
        "options": [opt.model_dump() for opt in opts],
        "presentation": presentation.dict()
    }