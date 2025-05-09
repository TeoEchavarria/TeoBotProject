import os
import logging
from typing import Dict, Any
from openai import OpenAI

from src.utils.strings import format_answer_with_parsed_json
from src.services.functions.response import SuggestionResponse
from src.services.functions.chapter import ChapterSection

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Initialize OpenAI Client ─────────────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ─── Main two‑step function ────────────────────────────────────────────────────
def answer_with_parsed_json(theme: str, language: str = "es") -> Dict[str, Any]:

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

The goal is to generate a clear, well-organized roadmap so the team knows exactly what to investigate, how to approach it, and how to maintain thematic coherence throughout the entire work. Stipulate a minimum of 20 chapters.
"""
            },
            {"role": "user", "content": theme},
        ],
        response_format=SuggestionResponse,
    )
    
    suggestions = resp1.choices[0].message.parsed
    opts = suggestions.options

    final_response = []

    for opt in opts:
        response_profile_content = """
    You are a renowned author of contemporary books, known for your sharp, thoughtful, and deeply human style. Although you have already published several successful works, you have always valued the guidance and intellectual challenges posed by one of your former mentors — someone who has been instrumental in shaping your growth and evolution as a writer.
    Dive deep into the key subtopics they’ve helped you identify.
    Bring your unique voice to transform those leads into vivid narrative, not just dry facts.
    Weave scattered threads together into a coherent, relevant, and compelling story for today’s reader.
    Keep your curiosity alive, always asking yourself the “why” and “what for” behind each section.
    """
        
        mentor_instructions = f"{opt.title} \n{opt.description} \n{opt.interesting_question} \n{opt.closing_paragraph}"
        
        messages = [
            {"role": "system", "content": response_profile_content},
            {"role": "system", "content": f"Response to {language}. "},
            {"role": "user", "content": mentor_instructions}
        ]

        
        resp2 = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            response_format= ChapterSection 
        )
        presentation = resp2.choices[0].message.parsed
        final_response.append(presentation.model_dump())

    return  final_response