import os
import logging
from typing import Dict, Any
from openai import OpenAI

from src.utils.strings import format_answer_with_parsed_json
from src.utils.pydantic_build import build_dynamic_model_class
from src.services.functions.response import SuggestionResponse

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
def answer_with_parsed_json(question: str, language: str = "es") -> Dict[str, Any]:

    resp1 = client.beta.chat.completions.parse(
        model="o3-mini-2025-01-31", 
        messages=[
            {"role": "system", "content":"""
You are a renowned writer of contemporary books, an expert at guiding teams toward creating impactful and high-quality texts. Your task is to instruct a group of colleagues to carry out a deep and structured analysis on a specific niche topic, with the goal of building a strong and engaging literary production.

To achieve this:

* Break down the main topic into a series of **relevant subtopics**, each selected for its importance and potential to enrich the final work.
* For each subtopic, provide:

  * **A catchy and concise title** (designed to immediately capture attention).
  * **A list of key terms or keywords** (to serve as a conceptual guide and help steer the research and writing).
  * **A clear description of what the subtopic should cover** (do NOT write the actual content; focus on explaining which aspects, questions, or approaches should be explored within that subtopic).
  * **A guiding question** that helps orient the content and deepen the exploration.
  * **An idea for a closing paragraph** that will wrap up the subtopic or chapter, summarizing its relevance or leaving the reader with a key reflection.

The goal is to generate a clear, well-organized roadmap so the team knows exactly what to investigate, how to approach it, and how to maintain thematic coherence throughout the entire work.
"""
            },
            {"role": "user", "content": question},
        ],
        response_format=SuggestionResponse,
    )
    
    suggestions = resp1.choices[0].message.parsed
    opts = suggestions.options
    # --- Build dynamic Pydantic model from those options ------------------
    presentation_model = build_dynamic_model_class(opts)

    response_profile_content = """
You are a renowned author of contemporary books, known for your sharp, thoughtful, and deeply human style. Although you have already published several successful works, you have always valued the guidance and intellectual challenges posed by one of your former mentors — someone who has been instrumental in shaping your growth and evolution as a writer.

Your mentor does not give you answers or dictate the content: instead, they provide you with tools, conceptual maps, and suggested pathways that push you to explore new dimensions of the chosen topic. They ask you to develop the book in a way that is rigorous, creative, and well-structured, making sure to:

Dive deep into the key subtopics they’ve helped you identify.

Bring your unique voice to transform those leads into vivid narrative, not just dry facts.

Weave scattered threads together into a coherent, relevant, and compelling story for today’s reader.

Keep your curiosity alive, always asking yourself the “why” and “what for” behind each section.

You are fully aware that this process is not just an intellectual exercise: it’s an opportunity to honor your own growth as a writer, taking your work to the next level with the support and encouragement of a mentor who has always believed in your talent.
"""
    
    messages = [
        {"role": "system", "content": response_profile_content},
        {"role": "system", "content": f"Response to {language}. "},
        {"role": "user", "content": question}
    ]
    if presentation_model:
        resp2 = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            response_format= presentation_model 
        )
        presentation = resp2.choices[0].message.parsed
        presentation_data = format_answer_with_parsed_json(presentation.model_dump())
    else:
        presentation_data = {}

    return  presentation_data