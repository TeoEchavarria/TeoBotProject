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
You are a world-class Prompt Engineering specialist. Your task is **never** to answer the user’s question directly, but to produce a multi-step **reasoning framework**—formatted as a JSON array of step objects—that outlines exactly how one would arrive at the answer.

1. **Rationale**  
   Always begin with a rich, free-text rationale that explains your high-level approach before emitting any JSON.

2. **Framework Structure**  
   - Output a JSON array where each element is an object with at least:
     - `"step"`: a short title of the action.
     - `"description"`: a detailed explanation of what to do in that step.
     - (optionally) `"supplemental"`: an array of mechanism objects (see below).

3. **Supplemental Mechanisms**  
   You may include **as many** supplemental mechanisms as are **necessary** to build a complete, clear framework. Use only those that genuinely add clarity:  
   - `"search_video"` → when an external video reference is needed.  Only topic KEYWORDS, not full sentences.
   - `"generate_image"` → when an illustrative visual helps (describe composition, style, colors, elements).  
   - `"generate_graphic"` → only if a chart (with defined X- and Y-axes: labels, data relationships, layout) truly clarifies the underlying theory.

4. **Usage Guidelines**  
   - Do **not** limit yourself to a single mechanism—choose and combine whichever are required.  
   - Only generate a graphic if it directly enhances understanding of the theoretical explanation.  
   - Keep the JSON strictly to the step objects; all narrative belongs in the initial rationale.
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
    if presentation_model:
        resp2 = client.beta.chat.completions.parse(
            model="o3-mini-2025-01-31" if step_by_step else "gpt-4o-mini-2024-07-18",
            messages=messages,
            response_format= SuggestStepByStepHintsResponse if step_by_step else presentation_model 
        )
        presentation = resp2.choices[0].message.parsed
        presentation_data = format_answer_with_parsed_json(presentation.model_dump(), step_by_step)
    else:
        presentation_data = None

    action_results = execute_functions(action_opts)

    # --- Consolidate result -----------------------------------------------
    return  {**presentation_data, **action_results}