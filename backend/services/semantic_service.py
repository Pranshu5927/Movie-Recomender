from embeddings.semantic_search import (
    semantic_search
)


class SemanticService:

    @staticmethod
    def search(
        query: str,
        limit: int = 10
    ):
        return semantic_search(
            query=query,
            top_k=limit
        )