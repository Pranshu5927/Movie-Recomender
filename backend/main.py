from fastapi import FastAPI
from sqlalchemy import text

from db.database import engine

from fastapi import Query

from api.auth import router as auth_router
from api.users import router as users_router
from api.ratings import router as ratings_router
from api.watchlist import router as watchlist_router
from api.recommendations import router as recommendations_router

app = FastAPI()

#  Authentication Router (/auth/login, /auth/signup)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

# Users Router (/me)
app.include_router(
    users_router,
    tags=["Users"]
)

# Ratings Router (/rate)
app.include_router(
    ratings_router,
    tags=["Ratings"]
)

# Watchlist Router (/watchlist/add, /watchlist, /watchlist/remove)
app.include_router(
    watchlist_router,
    tags=["Watchlist"]
)

# Recommendations Router (/recommendations)
app.include_router(
    recommendations_router,
    tags=["Recommendations"]
)

@app.get("/")
def home():
    return {"message": "Movie Recommender API is running"}


@app.get("/movies")
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


@app.get("/movies/search")
def search_movies(query: str = Query(...)):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT movie_id, title, genres
                FROM movies
                WHERE LOWER(title) LIKE LOWER(:query)
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