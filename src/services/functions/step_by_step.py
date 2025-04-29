from typing import List, Optional
from pydantic import BaseModel, field_validator


# ---- nested answer ------------------------------------------------------- #
class Answer(BaseModel):
    """Well-formed answer the learner should reconstruct."""
    summary: str
    explanation: str
    example: Optional[str] = None


# ---- single hint --------------------------------------------------------- #
class Hint(BaseModel):
    """One memory-triggering step."""
    memory_trigger: str 
    question: str
    answer: Answer


# ---- response wrapper ---------------------------------------------------- #
class SuggestStepByStepHintsResponse(BaseModel):
    """Between 4 and 7 hints, inclusive."""
    hints: List[Hint]