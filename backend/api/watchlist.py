from fastapi import APIRouter, Depends
from sqlalchemy import text

from db.database import engine
from utils.auth import get_current_user
from schemas.watchlist import WatchlistCreate

router = APIRouter()


# ---------------------------------
# ADD TO WATCHLIST
# ---------------------------------
@router.post("/watchlist/add")
def add_to_watchlist(
    watchlist_data: WatchlistCreate,
    current_user=Depends(get_current_user)
):

    with engine.connect() as connection:

        # Prevent duplicates
        existing = connection.execute(
            text("""
                SELECT *
                FROM watchlist
                WHERE user_id = :user_id
                AND movie_id = :movie_id
            """),
            {
                "user_id": current_user["id"],
                "movie_id": watchlist_data.movie_id
            }
        ).fetchone()

        if existing:
            return {
                "message": "Movie already in watchlist"
            }

        connection.execute(
            text("""
                INSERT INTO watchlist (
                    user_id,
                    movie_id
                )
                VALUES (
                    :user_id,
                    :movie_id
                )
            """),
            {
                "user_id": current_user["id"],
                "movie_id": watchlist_data.movie_id
            }
        )

        connection.commit()

    return {
        "message": "Movie added to watchlist"
    }


# ---------------------------------
# GET WATCHLIST
# ---------------------------------
@router.get("/watchlist")
def get_watchlist(
    current_user=Depends(get_current_user)
):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    movies.movie_id,
                    movies.title,
                    movies.genres
                FROM watchlist

                JOIN movies
                ON watchlist.movie_id = movies.movie_id

                WHERE watchlist.user_id = :user_id
            """),
            {
                "user_id": current_user["id"]
            }
        )

        movies = []

        for row in result:

            movies.append({
                "movie_id": row.movie_id,
                "title": row.title,
                "genres": row.genres
            })

    return movies


# ---------------------------------
# DELETE FROM WATCHLIST
# ---------------------------------
@router.delete("/watchlist/{movie_id}")
def remove_from_watchlist(
    movie_id: int,
    current_user=Depends(get_current_user)
):

    with engine.connect() as connection:

        connection.execute(
            text("""
                DELETE FROM watchlist
                WHERE user_id = :user_id
                AND movie_id = :movie_id
            """),
            {
                "user_id": current_user["id"],
                "movie_id": movie_id
            }
        )

        connection.commit()

    return {
        "message": "Movie removed from watchlist"
    }