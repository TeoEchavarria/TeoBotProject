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
) -> Optional[Type[BaseModel]]:
    text_fields: Dict[str, tuple] = {}

    for i, opt in enumerate(options):
        if opt.type != "text":
            continue

        # Determine the field name
        raw_key = f"step_{i+1}"
        key = raw_key.lower()

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