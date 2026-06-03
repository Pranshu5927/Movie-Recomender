from fastapi import FastAPI

from api.auth import router as auth_router
from api.users import router as users_router
from api.movies import router as movies_router
from api.ratings import router as ratings_router
from api.watchlist import router as watchlist_router
from api.recommendations import (
    router as recommendations_router
)
from api.semantic import router as semantic_router

app = FastAPI()


# ---------------------------------
# AUTH ROUTES
# ---------------------------------
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


# ---------------------------------
# USER ROUTES
# ---------------------------------
app.include_router(
    users_router,
    tags=["Users"]
)


# ---------------------------------
# MOVIE ROUTES
# ---------------------------------
app.include_router(
    movies_router,
    tags=["Movies"]
)


# ---------------------------------
# RATINGS ROUTES
# ---------------------------------
app.include_router(
    ratings_router,
    tags=["Ratings"]
)


# ---------------------------------
# WATCHLIST ROUTES
# ---------------------------------
app.include_router(
    watchlist_router,
    tags=["Watchlist"]
)


# ---------------------------------
# RECOMMENDATION ROUTES
# ---------------------------------
app.include_router(
    recommendations_router,
    tags=["Recommendations"]
)

# ---------------------------------
# SEMANTIC SEARCH ROUTES
# ---------------------------------
app.include_router(
    semantic_router
)

# ---------------------------------
# HEALTH CHECK
# ---------------------------------
@app.get("/")
def home():

    return {
        "message": "Movie Recommender API is running"
    }