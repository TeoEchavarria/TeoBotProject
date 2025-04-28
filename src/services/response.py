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

    resp1 = client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content":"""
You are a world-class Prompt Engineering specialist. Your goal is to generate, for any user question, a multi-step response framework—not the answer itself—formatted as a JSON array of step objects.

Overall requirements  
- Don't answer the user's question; just generate the framework, the reasoning for how to answer that question.  
- Always start with a rich, free-text rationale before deciding on any supplemental mechanism.  
- Allow at most one supplemental mechanism:  
  - "search_video" if you need external video clarifications.
  - "generate_image" if you need an illustrative visual (describe composition, style, colors, and elements).  
  - "generate_graphic" only if you need a chart with defined X- and Y-axes (specify axis labels, data relationships, layout).  
"""
            },
            {"role": "user", "content": question},
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
    
    messages = [
        {"role": "system", "content": response_profile_content},
        {"role": "system", "content": f"Response to {language}."},
        {"role": "user", "content": question}
    ]

    resp2 = client.beta.chat.completions.parse(
        model="o3-mini-2025-01-31" if step_by_step else "gpt-4o-mini-2024-07-18",
        messages=messages,
        response_format= SuggestStepByStepHintsResponse if step_by_step else presentation_model 
    )
    presentation = resp2.choices[0].message.parsed

    action_results = execute_functions(action_opts)

    # --- Consolidate result -----------------------------------------------
    presentation_data = format_answer_with_parsed_json(presentation.model_dump(), step_by_step)
    return  {**presentation_data, **action_results}