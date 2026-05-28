from pydantic import BaseModel


class WatchlistCreate(BaseModel):
    movie_id: int