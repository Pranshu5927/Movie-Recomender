from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Recommendation(BaseModel):
    movie_id: int
    title: str
    genres: str

    score: float
    normalized_score: float

    recommendation_source: str

    vote_count: Optional[int] = None

    reasons: List[str] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(default_factory=dict)