from fastapi import APIRouter

from ai.query_parser import parse_user_query
from ai.recommendation_pipeline import retrieve_candidates
from ai.reranker import rerank_movies
from ai.explanation_generator import generate_explanation
from ai.schemas import AIRecommendationResponse


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get(
    "/recommend",
    response_model=AIRecommendationResponse
)
def recommend(query: str):

    # ---------------------------------
    # PARSE QUERY
    # ---------------------------------
    parsed = parse_user_query(query)


    # ---------------------------------
    # RETRIEVE CANDIDATES
    # ---------------------------------
    candidates = retrieve_candidates(
        raw_query=query,
        parsed=parsed
    )


    # ---------------------------------
    # AI RE-RANK
    # ---------------------------------
    movies = rerank_movies(
        query=query,
        candidates=candidates
    )


    # ---------------------------------
    # GENERATE EXPLANATION
    # ---------------------------------
    explanation = generate_explanation(
        query=query,
        movies=movies[:5]
    )


    return AIRecommendationResponse(
        query=query,
        explanation=explanation,
        movies=movies[:10]
    )
