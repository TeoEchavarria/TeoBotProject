from pydantic import BaseModel, create_model
from src.utils.strings import normalize_key

def build_dynamic_model_class(options, step_by_step : bool) -> type[BaseModel]:
    """
    Create a Pydantic model where each normalized 'option.title' is a required str field.
    """
    fields = {}
    for opt in options:
        if not step_by_step:
            key = normalize_key(opt.title)
            fields[key] = (str, ...)
        else:
            fields[opt.title] = (str, ...)
    return create_model("PresentationResponse", __base__=BaseModel, **fields)
