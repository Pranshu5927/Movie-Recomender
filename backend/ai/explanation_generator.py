from typing import List

from ai.llm_service import chat


SYSTEM_PROMPT = """You are a concise movie recommendation assistant.
Explain recommendations in 2-3 sentences. Be specific about themes,
tone, and what makes each film a good match. Do not use bullet points."""


def generate_explanation(
    query: str,
    movies: List[dict]
) -> str:

    if not movies:
        return "Here are some movies that match your request."

    movie_lines = [
        f"- {m['title']} ({m['genres']})"
        for m in movies
    ]

    movie_text = "\n".join(movie_lines)

    prompt = f"""User asked for: {query}

Top recommendations:
{movie_text}

Explain in 2-3 sentences why these films match the request.
Reference specific themes, tones, or qualities."""

    try:

        return chat(
            [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4
        )

    except Exception:

        return "Here are some movies that match your request."
