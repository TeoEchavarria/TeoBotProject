from pydantic import BaseModel, create_model
from src.utils.strings import normalize_key
from typing import Dict, Type, Any, Optional

# ─── Import custom functions ────────────────────────────────────────────────
from src.services.search_video import youtube_search
from src.services.generate_image import generate_image
from src.services.generate_graphic import chart_code

def build_dynamic_model_class(options, step_by_step: bool) -> Optional[Type[BaseModel]]:
    text_fields: Dict[str, tuple] = {}
    for opt in options:
        if opt.type != "text":
            continue
        key = opt.title if step_by_step else normalize_key(opt.title)
        text_fields[key] = (str, ...)

    if not text_fields:
        return None  # caller must handle this case

    return create_model("PresentationResponse", __base__=BaseModel, **text_fields)

def execute_functions(action_opts):
    action_results: Dict[str, Any] = {}
    for opt in action_opts:
        key = normalize_key(opt.title)
        try:
            if opt.type == "search_video":
                videos = youtube_search(query=opt.description or opt.title, max_results=1)
                action_results[key] = videos[0]["url"] if videos else None
            elif opt.type == "generate_image":
                img_path = generate_image(prompt=opt.description or opt.title)
                action_results[key] = str(img_path)
            elif opt.type == "generate_graphic":
                chart_path = chart_code(requirement=opt.description or opt.title)
                action_results[key] = str(chart_path)
            else:  # pragma: no cover – should not occur
                action_results[key] = None
        except Exception as e:  # keep flow even if one action fails
            action_results[key] = {"error": str(e)}
    
    return action_results