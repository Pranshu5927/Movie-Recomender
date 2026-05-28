from fastapi import APIRouter, Depends

from utils.auth import get_current_user
from recommender.popularity import get_popular_recommendations

router = APIRouter()


@router.get("/recommendations")
def recommendations(
    current_user=Depends(get_current_user)
):

    recommendations = get_popular_recommendations(
        current_user["id"]
    )

    return recommendations