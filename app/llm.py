from google.genai import types

from app.config import settings
from app.gemini_client import client

DEFAULT_SYSTEM_PROMPT = (
    "You are ResolveAgent, a helpful assistant for customers of a payments company. "
    "Answer clearly in 3 to 5 sentences. "
    "If you are not sure about something, say so instead of guessing."
)


def generate(prompt: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> dict:
    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    usage = response.usage_metadata
    return {
        "answer": response.text,
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
    }