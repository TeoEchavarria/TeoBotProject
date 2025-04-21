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
    logger.info("Question: %s", question)

    # --- Step 1: Suggest presentation formats, parsed as JSON --------------
    resp1 = client.beta.chat.completions.parse(
        model="o3-mini-2025-01-31",
        messages=[
            {"role": "system", "content":
                "Extract creative presentation options. "
                "Return a JSON object with an 'options' array of {title, description, type}."
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
        model="gpt-4o-search-preview-2025-03-11",
        messages=[
            {"role": "system", "content":
                "Generate a JSON object with keys exactly matching the earlier option titles "
                "(in snake_case), each value a string presenting the solution in that style."
            },
            {"role": "user", "content": question}
        ],
        response_format=PresentationModel
    )
    presentation: PresentationModel = resp2.choices[0].message.parsed

    # --- Consolidate result -----------------------------------------------
    return {
        "options": [opt.dict() for opt in opts],
        "presentation": presentation.dict()
    }

# ─── Example Usage ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    q = "Explain what a neural network is, using varied presentation styles."
    result = answer_with_parsed_json(q)
    print(json.dumps(result, indent=2, ensure_ascii=False))
