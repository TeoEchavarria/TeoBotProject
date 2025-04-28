from typing import List, Dict, Any
from typing_extensions import Literal
from pydantic import BaseModel

class SuggestionOption(BaseModel):
    title: str
    description: str
    type: Literal["string", "number", "integer", "boolean", "object", "array"]

class SuggestionResponse(BaseModel):
    options: List[SuggestionOption]