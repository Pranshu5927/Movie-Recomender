from fastapi import APIRouter, Query

from sqlalchemy import text

from db.database import engine


router = APIRouter()


# ---------------------------------
# GET MOVIES
# ---------------------------------
@router.get("/movies")
def get_movies():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT movie_id, title, genres
                FROM movies
                LIMIT 20
            """)
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
# SEARCH MOVIES
# ---------------------------------
@router.get("/movies/search")
def search_movies(query: str = Query(...)):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT movie_id, title, genres
                FROM movies
                WHERE LOWER(title)
                LIKE LOWER(:query)
                LIMIT 20
            """),
            {
                "query": f"%{query}%"
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