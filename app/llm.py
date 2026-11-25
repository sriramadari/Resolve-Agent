from google import genai
from google.genai import types

from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

SYSTEM_PROMPT = (
    "You are ResolveAgent, a helpful assistant for customers of a payments company. "
    "Answer clearly in 3 to 5 sentences. "
    "If you are not sure about something, say so instead of guessing."
)


def ask_llm(question: str) -> dict:
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    usage = response.usage_metadata
    return {
        "answer": response.text,
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
    }