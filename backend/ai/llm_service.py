import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def chat(messages: list, temperature: float = 0.2) -> str:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content
