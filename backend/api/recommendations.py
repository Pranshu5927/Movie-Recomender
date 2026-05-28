from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from utils.auth import get_current_user

from services.recommendation_service import (
    get_homepage_recommendations,
    get_content_based_recommendations
)

router = APIRouter()


# ---------------------------------
# NETFLIX HOMEPAGE
# ---------------------------------
@router.get("/recommendations")
def recommendations(
    current_user=Depends(get_current_user)
):

    recommendations = (
        get_homepage_recommendations(
            current_user["id"]
        )
    )

    return recommendations


# ---------------------------------
# MORE LIKE THIS
# ---------------------------------
@router.get("/recommendations/content")
def content_recommendations(
    movie_title: str = Query(...)
):

    recommendations = (
        get_content_based_recommendations(
            movie_title
        )
    )

    return recommendations