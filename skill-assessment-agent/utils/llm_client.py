import os
from openai import OpenAI
from utils.config import (
    LLM_PROVIDER, GROQ_API_KEY, OPENAI_API_KEY,
    GOOGLE_API_KEY, MODEL_NAME
)


def get_llm_client():
    if LLM_PROVIDER == "groq":
        if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_your"):
            raise ValueError(
                "Set a valid GROQ_API_KEY in .env. "
                "Get one free at https://console.groq.com"
            )
        return OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
    elif LLM_PROVIDER == "google":
        if not GOOGLE_API_KEY or GOOGLE_API_KEY.startswith("your_"):
            raise ValueError(
                "Set a valid GOOGLE_API_KEY in .env. "
                "Get one free at https://aistudio.google.com"
            )
        return OpenAI(
            api_key=GOOGLE_API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    elif LLM_PROVIDER == "openai":
        return OpenAI(api_key=OPENAI_API_KEY)
    elif LLM_PROVIDER == "ollama":
        return OpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1"
        )
    elif LLM_PROVIDER == "openrouter":
        return OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            base_url="https://openrouter.ai/api/v1"
        )
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def get_model_name():
    return MODEL_NAME


def create_completion(messages, temperature=0.3, json_mode=True):
    client = get_llm_client()
    kwargs = {
        "model": get_model_name(),
        "messages": messages,
        "temperature": temperature,
    }
    if json_mode and LLM_PROVIDER in ("openai", "groq"):
        kwargs["response_format"] = {"type": "json_object"}
    elif json_mode and LLM_PROVIDER == "google":
        if messages and messages[0]["role"] == "system":
            messages[0]["content"] += (
                "\nIMPORTANT: Respond ONLY with valid JSON."
            )
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content
