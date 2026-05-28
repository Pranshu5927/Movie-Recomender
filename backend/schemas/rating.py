from pydantic import BaseModel


class RatingCreate(BaseModel):
    movie_id: int
    rating: float