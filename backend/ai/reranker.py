import json

from typing import List

from ai.llm_service import chat


SYSTEM_PROMPT = """You are a movie recommendation expert.
Rank candidate movies based on how well they match the user's query.
Return a JSON array of movie_ids only. No explanation, no markdown."""


def rerank_movies(
    query: str,
    candidates: List[dict],
    top_n: int = 10
) -> List[dict]:

    if not candidates:
        return []


    # ---------------------------------
    # BUILD CANDIDATE LIST FOR PROMPT
    # ---------------------------------
    candidate_lines = []

    for movie in candidates:
        candidate_lines.append(
            f"{movie['movie_id']}: {movie['title']} | {movie['genres']}"
        )

    candidate_text = "\n".join(candidate_lines)


    # ---------------------------------
    # LLM RANKING
    # ---------------------------------
    prompt = f"""User query: {query}

Candidate movies (movie_id: title | genres):
{candidate_text}

Return a JSON array of the top {top_n} movie_ids ranked from best match to worst.
Return ONLY the JSON array. Example: [123, 456, 789]"""

    try:

        result = chat([
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ])

        ranked_ids = json.loads(result)

        if not isinstance(ranked_ids, list):
            return candidates[:top_n]


        # ---------------------------------
        # REORDER CANDIDATES BY LLM RANK
        # ---------------------------------
        candidate_lookup = {
            movie["movie_id"]: movie
            for movie in candidates
        }

        reranked = []

        for movie_id in ranked_ids:
            if movie_id in candidate_lookup:
                reranked.append(
                    candidate_lookup[movie_id]
                )

        # Append any candidates the LLM missed
        # so the list always has top_n entries
        seen_ids = set(ranked_ids)

        for movie in candidates:
            if len(reranked) >= top_n:
                break
            if movie["movie_id"] not in seen_ids:
                reranked.append(movie)

        return reranked[:top_n]

    except (json.JSONDecodeError, Exception):

        return candidates[:top_n]
