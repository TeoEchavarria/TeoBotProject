import os
import logging
from typing import Dict, Any
from openai import OpenAI

from src.utils.strings import normalize_key
from src.utils.pydantic_build import build_dynamic_model_class
from src.services.functions.response import SuggestionResponse
from src.services.functions.step_by_step import SuggestStepByStepHintsResponse

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Initialize OpenAI Client ─────────────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Main two‑step function ────────────────────────────────────────────────────
def answer_with_parsed_json(question: str, step_by_step : bool) -> Dict[str, Any]:
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
        response_format= SuggestStepByStepHintsResponse if step_by_step else SuggestionResponse,
    )
    suggestions = resp1.choices[0].message.parsed
    opts = suggestions.options
    logger.info("Received %d options", opts)

    # --- Build dynamic Pydantic model from those options ------------------
    presentation_model = build_dynamic_model_class(opts, step_by_step)

    # --- Step 2: Force JSON response matching dynamic model ---------------

    messages = [
        {"role": "system", "content":
            "Response in a smooth, short, bold and expert manner. Only return the most valuable and relevant information."
        }
    ]

    if step_by_step:
        messages.append({"role": "user", "content": question})
    else:
        messages.append({"role": "user", "content": question + "\n".join([opt.model_dump()["description"] for opt in opts])})
    resp2 = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        response_format=presentation_model
    )
    presentation = resp2.choices[0].message.parsed

    # --- Consolidate result -----------------------------------------------
    return {opt.title: presentation.model_dump()[opt.title if step_by_step else normalize_key(opt.title) ] for opt in opts}