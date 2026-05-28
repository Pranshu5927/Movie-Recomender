from fastapi import APIRouter, Depends
from sqlalchemy import text

from db.database import engine
from utils.auth import get_current_user
from schemas.rating import RatingCreate

router = APIRouter()


@router.post("/rate")
def rate_movie(
    rating_data: RatingCreate,
    current_user=Depends(get_current_user)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                INSERT INTO ratings (
                    user_id,
                    movie_id,
                    rating
                )
                VALUES (
                    :user_id,
                    :movie_id,
                    :rating
                )
            """),
            {
                "user_id": current_user["id"],
                "movie_id": rating_data.movie_id,
                "rating": rating_data.rating
            }
        )

        connection.commit()

    return {
        "message": "Rating added successfully"
    }