from pydantic import BaseModel, create_model
from typing import Dict, Type, Any, Optional
import logging

# ─── Import custom functions ────────────────────────────────────────────────
from src.services.search_video import youtube_search
from src.services.search_diagrams import search_diagram
from src.services.generate_graphic import chart_code

from typing import Dict, Optional, Type
from pydantic import BaseModel, create_model, Field

def build_dynamic_model_class(
    options: list["SuggestionOption"],
    step_by_step: bool
) -> Optional[Type[BaseModel]]:
    text_fields: Dict[str, tuple] = {}

    for i, opt in enumerate(options):
        if opt.type != "text":
            continue

        # Determine the field name
        raw_key = f"step_{i+1}"
        key = raw_key if step_by_step else raw_key.lower()

        # Use Field to attach the human-readable description
        text_fields[key] = (
            str,
            Field(
                ...,
                description=opt.description
            )
        )

    if not text_fields:
        return None  # caller must handle absence of text steps

    # Dynamically create a model named "PresentationResponse"
    return create_model(
        "PresentationResponse",
        __base__=BaseModel,
        **text_fields
    )


def execute_functions(action_opts, language: str = "es", question : str = "") -> Dict[str, Any]:
    action_results = {
        "search_video": [],
        "search_diagrams": [],
        "generate_graphic": [],
    }
    for opt in action_opts:
        try:
            if opt.type == "search_video":
                videos = youtube_search(query=f"{question} {opt.description}", max_results=1, language=language)
                action_results[opt.type].append(videos[0]["url"] if videos else None)
            elif opt.type == "search_diagrams":
                img_path = search_diagram(keywords=f"{question} {opt.description}")
                if img_path is not None:
                    action_results[opt.type].append(str(img_path))
            elif opt.type == "generate_graphic":
                chart_path = chart_code(requirement=opt.description)
                action_results[opt.type].append(str(chart_path))
        except Exception as e:  # keep flow even if one action fails
            logging.error(f"Error executing function for {opt.type}: {e}")
            action_results[opt.type].append(None)
    
    return action_results