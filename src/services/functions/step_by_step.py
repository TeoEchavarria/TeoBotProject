from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class Hint(BaseModel):
    title: str = Field(
        ...,
        description="A short, descriptive title for the hint.",
    )
    hint: str = Field(
        ...,
        description="A concise clue or prompt that nudges the user toward the solution.",
    )


class SuggestStepByStepHintsResponse(BaseModel):
    options: List[Hint]
