from typing import List

from embeddings.semantic_search import semantic_search

from recommender.content_based import get_similar_movies

from recommender.popularity import get_popular_recommendations

from ai.schemas import ParsedMovieQuery


def retrieve_candidates(
    raw_query: str,
    parsed: ParsedMovieQuery
) -> List[dict]:

    candidates: dict[int, dict] = {}


    # ---------------------------------
    # SEMANTIC SEARCH
    # Always run against the raw query.
    # ---------------------------------
    try:

        semantic_results = semantic_search(
            raw_query,
            top_k=20
        )

        for movie in semantic_results:
            candidates[movie["movie_id"]] = movie

    except Exception:
        pass


    # ---------------------------------
    # CONTENT-BASED (similar_to titles)
    # ---------------------------------
    for title in parsed.similar_to:

        try:

            similar = get_similar_movies(title)

            for movie in similar:
                if movie["movie_id"] not in candidates:
                    candidates[movie["movie_id"]] = movie

        except (IndexError, KeyError, Exception):
            pass


    # ---------------------------------
    # POPULARITY FALLBACK
    # Fills the pool when semantic /
    # content-based yield few results.
    # user_id=0 excludes nothing.
    # ---------------------------------
    try:

        popular = get_popular_recommendations(
            user_id=0
        )

        for movie in popular:
            if movie["movie_id"] not in candidates:
                candidates[movie["movie_id"]] = movie

    except Exception:
        pass


    return list(candidates.values())[:50]


def run_recommendation_pipeline(intent: str) -> List[dict]:

    from ai.query_parser import parse_user_query
    from ai.reranker import rerank_movies

    parsed = parse_user_query(intent)

    candidates = retrieve_candidates(intent, parsed)

    movies = rerank_movies(intent, candidates)

    return movies
