import requests
import os
from typing import Optional

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_TIMEOUT_S = float(os.getenv("OLLAMA_TIMEOUT_S", "15"))

def generate_response(prompt: str, *, system: Optional[str] = None) -> str:
    full_prompt = prompt if not system else f"{system}\n\n{prompt}"
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
            },
            timeout=OLLAMA_TIMEOUT_S,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip() or "I didn't get a response from the model."
    except Exception:
        # Keep UX responsive (Phase 1 requirement: avoid long LLM delays)
        return (
            "LLM is currently unavailable. Start Ollama and pull a model, then try again.\n"
            "Example: `ollama run mistral`"
        )


# alias
def ask_ollama(prompt: str) -> str:
    return generate_response(prompt)