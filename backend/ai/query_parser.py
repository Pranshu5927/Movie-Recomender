import json

from ai.llm_service import chat
from ai.schemas import ParsedMovieQuery


SYSTEM_PROMPT = """You are a movie query parser.
Extract movie recommendation intent from the user's query.
Return valid JSON only. No explanation, no markdown, no code blocks."""


def parse_user_query(query: str) -> ParsedMovieQuery:

    prompt = f"""Extract movie recommendation intent.

Return JSON only.

User Query:
{query}

Schema:

{{
    "genres": [],
    "moods": [],
    "themes": [],
    "similar_to": [],
    "exclude": []
}}

Rules:
- genres: standard movie genre names (Action, Comedy, Drama, Sci-Fi, Thriller, Horror, etc.)
- moods: emotional tones (dark, funny, uplifting, tense, romantic, etc.)
- themes: subject matter (space, time travel, family, revenge, war, etc.)
- similar_to: specific movie titles the user referenced
- exclude: genres or tones to avoid"""

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

        parsed = json.loads(result)

        return ParsedMovieQuery(**parsed)

    except (json.JSONDecodeError, Exception):

        return ParsedMovieQuery()
