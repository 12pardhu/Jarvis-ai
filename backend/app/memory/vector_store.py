from __future__ import annotations

import json
import os
import time
from pathlib import Path

# Phase 0/1 stability note:
# Chroma currently breaks on Python 3.13 in this repo environment.
# To keep the system working end-to-end, we use a lightweight local JSONL store.

_DEFAULT_PATH = Path(os.getenv("JARVIS_MEMORY_PATH", "data/memory.jsonl"))
_MAX_LINES = int(os.getenv("JARVIS_MEMORY_MAX_LINES", "2000"))

def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def add_memory(text: str) -> None:
    text = (text or "").strip()
    if not text:
        return

    path = _DEFAULT_PATH
    _ensure_parent(path)
    record = {"ts": time.time(), "text": text}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Simple cap (keeps file small for demos)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > _MAX_LINES:
            path.write_text("\n".join(lines[-_MAX_LINES:]) + "\n", encoding="utf-8")
    except Exception:
        pass

def search_memory(query: str, *, n_results: int = 3) -> list[str]:
    query = (query or "").strip().lower()
    if not query:
        return []

    path = _DEFAULT_PATH
    if not path.exists():
        return []

    # Naive relevance: substring hit score + recency tie-break.
    hits: list[tuple[int, float, str]] = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            text = str(obj.get("text", ""))
            ts = float(obj.get("ts", 0.0))
            t = text.lower()
            score = 0
            if query in t:
                score += 5
            # small bonus for shared keywords
            q_words = [w for w in query.split() if len(w) >= 3]
            score += sum(1 for w in q_words if w in t)
            if score > 0:
                hits.append((score, ts, text))
    except Exception:
        return []

    hits.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [h[2] for h in hits[: max(1, n_results)]]