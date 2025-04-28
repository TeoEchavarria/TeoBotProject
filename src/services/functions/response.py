from typing import List
from typing_extensions import Literal
from pydantic import BaseModel

class SuggestionOption(BaseModel):
    description: str
    type: Literal["text", "search_video", "generate_image", "generate_graphic" ]

class SuggestionResponse(BaseModel):
    options: List[SuggestionOption]