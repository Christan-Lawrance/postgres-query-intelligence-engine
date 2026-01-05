# '''
# This class defines a strict schema for LLM-generated recommendations and validates them before you trust or store them.

# In short:
# LLM talks → raw text
# Pydantic checks → structured truth
# DB stores → safe data

# This is exactly how LLMs should be used in production.
# '''


from pydantic import BaseModel, Field


class LLMRecommendationSchema(BaseModel):
    summary: str = Field(min_length=10, max_length=100)
    details: str = Field(min_length=20)
    confidence_score: float = Field(ge=0.0, le=1.0)
