from __future__ import annotations

import re

from app.voice.translation import get_translator

_translator = get_translator()

_DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")  # Hindi
_TELUGU_RE = re.compile(r"[\u0C00-\u0C7F]")      # Telugu

def detect_language(text: str) -> str:
    """
    Fast, offline detection limited to en/hi/te (sufficient for project scope).
    """
    text = text or ""
    if _TELUGU_RE.search(text):
        return "te"
    if _DEVANAGARI_RE.search(text):
        return "hi"
    return "en"

def translate_to_english(text: str, *, source_lang: str) -> str:
    # LibreTranslate expects "en"/"hi"/"te" codes
    return _translator.translate(text or "", source=source_lang, target="en")

def translate_from_english(text: str, *, target_lang: str) -> str:
    return _translator.translate(text or "", source="en", target=target_lang)