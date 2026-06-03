from typing import List

from ai.llm_service import chat

from agents.prompts import SYSTEM_PROMPT, INTENT_EXTRACTION_PROMPT


def understand_user_intent(
    message: str,
    history: List[dict]
) -> str:

    # ---------------------------------
    # BUILD CONVERSATION CONTEXT
    # ---------------------------------
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for msg in history:
        messages.append({
            "role": msg.role if hasattr(msg, "role") else msg["role"],
            "content": msg.content if hasattr(msg, "content") else msg["content"]
        })

    messages.append({
        "role": "user",
        "content": message
    })


    # ---------------------------------
    # EXTRACT STANDALONE INTENT
    # The model sees the full conversation
    # and distills it into a search query.
    # ---------------------------------
    messages.append({
        "role": "user",
        "content": INTENT_EXTRACTION_PROMPT
    })

    intent = chat(messages, temperature=0.1)

    return intent.strip()
