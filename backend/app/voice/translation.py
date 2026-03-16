from __future__ import annotations

import os
from typing import Protocol

import requests


class Translator(Protocol):
    def translate(self, text: str, *, source: str, target: str) -> str: ...


class NoopTranslator:
    def translate(self, text: str, *, source: str, target: str) -> str:
        return text or ""


class LibreTranslateTranslator:
    """
    Uses a LibreTranslate-compatible API.
    Configure:
      - JARVIS_TRANSLATE_URL (default: http://localhost:5000/translate)
      - JARVIS_TRANSLATE_API_KEY (optional)
      - JARVIS_TRANSLATE_TIMEOUT_S (default: 5)
    """

    def __init__(self) -> None:
        self.url = os.getenv("JARVIS_TRANSLATE_URL", "http://localhost:5000/translate")
        self.api_key = os.getenv("JARVIS_TRANSLATE_API_KEY", "")
        self.timeout_s = float(os.getenv("JARVIS_TRANSLATE_TIMEOUT_S", "5"))

    def translate(self, text: str, *, source: str, target: str) -> str:
        text = (text or "").strip()
        if not text or source == target:
            return text
        payload = {"q": text, "source": source, "target": target, "format": "text"}
        if self.api_key:
            payload["api_key"] = self.api_key
        try:
            r = requests.post(self.url, json=payload, timeout=self.timeout_s)
            r.raise_for_status()
            data = r.json()
            return (data.get("translatedText") or "").strip() or text
        except Exception:
            # Fail open: never block assistant on translation
            return text


def get_translator() -> Translator:
    provider = os.getenv("JARVIS_TRANSLATE_PROVIDER", "noop").strip().lower()
    if provider in ("libretranslate", "libre", "lt"):
        return LibreTranslateTranslator()
    return NoopTranslator()

