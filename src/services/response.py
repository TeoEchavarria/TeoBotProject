import os
import logging
from typing import Dict, Any
from openai import OpenAI

from src.utils.strings import format_answer_with_parsed_json
from src.utils.pydantic_build import build_dynamic_model_class, execute_functions
from src.services.functions.response import SuggestionResponse
from src.services.functions.step_by_step import SuggestStepByStepHintsResponse

def _read_profile_file(file_type: str, profile: str) -> str:
    """Helper function to read profile files with fallback to default"""
    path = f"src/services/voices/{file_type}/{profile}.txt"
    default_path = f"src/services/voices/{file_type}/default.txt"
    
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read().strip()
        else:
            with open(default_path, 'r') as f:
                return f.read().strip()
    except Exception as e:
        logger.error(f"Error reading profile file: {e}")
        return ""

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Initialize OpenAI Client ─────────────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Main two‑step function ────────────────────────────────────────────────────
def answer_with_parsed_json(question: str, step_by_step : bool, language: str = "Spanish", profile : str = "default") -> Dict[str, Any]:

    # --- Step 1: Suggest presentation formats, parsed as JSON --------------
    # --- Step 1: Get presentation formats as JSON -------------------------
    start_profile_content = _read_profile_file("start", profile)
    
    resp1 = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content":
                f"Design an optimal response framework by listing the steps (mechanisms) you would follow to answer a complex question. {start_profile_content} For each step, include 1. The name of the mechanism. 2. Its purpose. 3. A brief justification. What kind of content the mechanism should return."
            }
        ],
        response_format=SuggestionResponse,
    )
    
    suggestions = resp1.choices[0].message.parsed
    opts = suggestions.options

    text_opts = [o for o in opts if o.type == "text"]
    action_opts = [o for o in opts if o.type != "text"]
    
    # --- Build dynamic Pydantic model from those options ------------------
    presentation_model = build_dynamic_model_class(text_opts, step_by_step)

    # --- Step 2: Force JSON response matching dynamic model ---------------
    response_profile_content = _read_profile_file("response", profile)
    
    option_descriptions = "\n".join([opt.model_dump()["description"] for opt in opts]) if opts else ""
    user_content = f"{question}\n\n{option_descriptions}" if option_descriptions else question
    
    messages = [
        {"role": "system", "content": response_profile_content},
        {"role": "system", "content": f"Response to {language}."},
        {"role": "user", "content": user_content}
    ]

    resp2 = client.beta.chat.completions.parse(
        model="o3-mini-2025-01-31" if step_by_step else "gpt-4o-mini-2024-07-18",
        messages=messages,
        response_format= SuggestStepByStepHintsResponse if step_by_step else presentation_model 
    )
    presentation = resp2.choices[0].message.parsed

    action_results = execute_functions(action_opts)

    # --- Consolidate result -----------------------------------------------
    presentation_data = format_answer_with_parsed_json(presentation, step_by_step)
    return  {**presentation_data, **action_results}