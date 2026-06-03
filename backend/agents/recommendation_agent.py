from agents.chatbot import understand_user_intent

from ai.recommendation_pipeline import run_recommendation_pipeline

from ai.explanation_generator import generate_explanation


def handle_chat(
    message: str,
    history: list
) -> dict:

    # ---------------------------------
    # STEP 1 — UNDERSTAND INTENT
    # Combines full conversation history
    # with current message into a single
    # standalone search query.
    # ---------------------------------
    intent = understand_user_intent(
        message,
        history
    )


    # ---------------------------------
    # STEP 2 — GET RECOMMENDATIONS
    # Runs: parse → retrieve → rerank
    # ---------------------------------
    movies = run_recommendation_pipeline(intent)


    # ---------------------------------
    # STEP 3 — GENERATE EXPLANATION
    # LLM writes a 2-3 sentence response
    # grounded in the top results.
    # ---------------------------------
    explanation = generate_explanation(
        intent,
        movies[:5]
    )


    return {
        "reply": explanation,
        "movies": movies[:10]
    }
