from typing import List, Optional
from pydantic import BaseModel, Field


class ChapterSection(BaseModel):
    # Core narrative
    introduction: str = Field(
        ...,
        description="Brief opener that hooks the reader and frames the topic."
    )
    concepts_explanation: str = Field(
        ...,
        description="Definitions and clarification of the key concepts."
    )
    idea_development: str = Field(
        ...,
        description="Argument development: analysis, evidence, and examples."
    )
    complement: str = Field(
        ...,
        description="Supplementary material: case studies, charts, anecdotes."
    )
    authors_and_sources: str = Field(
        ...,
        description="Authors, studies, or references supporting the chapter."
    )
    closing_paragraph: str = Field(
        ...,
        description="Closing that bridges to the next chapter or summarises key ideas."
    )

    # Enrichment & pedagogy (all optional)
    learning_objectives: Optional[List[str]] = Field(
        None,
        description="Specific outcomes readers should achieve after this chapter."
    )
    overview: Optional[str] = Field(
        None,
        description="Concise roadmap of the chapter’s main points."
    )
    key_terms: Optional[List[str]] = Field(
        None,
        description="Important vocabulary introduced in this chapter."
    )
    epigraph: Optional[str] = Field(
        None,
        description="A quotation that sets the tone or theme."
    )
    reflection_questions: Optional[List[str]] = Field(
        None,
        description="Prompts for self-reflection or group discussion."
    )
    exercises: Optional[List[str]] = Field(
        None,
        description="Practice activities or mini-assessments."
    )
    visuals: Optional[List[str]] = Field(
        None,
        description="IDs/paths of figures, diagrams, or tables to embed."
    )
    key_takeaways: Optional[List[str]] = Field(
        None,
        description="Bullet-point summary of essential ideas."
    )
    further_reading: Optional[List[str]] = Field(
        None,
        description="Curated list of articles, books, or multimedia for deeper study."
    )
    footnotes: Optional[str] = Field(
        None,
        description="Detailed citations or commentary kept out of the main text."
    )