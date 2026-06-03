from pydantic import BaseModel
from typing import List


class ParsedMovieQuery(BaseModel):
    genres: List[str] = []
    moods: List[str] = []
    themes: List[str] = []
    similar_to: List[str] = []
    exclude: List[str] = []


class AIRecommendationResponse(BaseModel):
    query: str
    explanation: str
    movies: list
