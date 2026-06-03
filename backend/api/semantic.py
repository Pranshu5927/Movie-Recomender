from fastapi import APIRouter

from services.semantic_service import (
    SemanticService
)

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)

@router.get("/semantic")
def semantic_search_endpoint(
    query: str,
    limit: int = 10
):

    results = SemanticService.search(
        query=query,
        limit=limit
    )

    return {
        "query": query,
        "results": results
    }