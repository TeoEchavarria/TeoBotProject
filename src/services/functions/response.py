from typing import List
from typing_extensions import Literal
from pydantic import BaseModel

class SuggestionOption(BaseModel):
    title: str
    keywords: List[str]
    description: str
    interesting_question : str
    closing_paragraph : str

class SuggestionResponse(BaseModel):
    options: List[SuggestionOption]