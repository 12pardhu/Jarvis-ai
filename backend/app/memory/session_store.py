from __future__ import annotations

import os
import threading
import time
import uuid
from dataclasses import dataclass

_MAX_TURNS = int(os.getenv("JARVIS_CONTEXT_TURNS", "8"))  # user+assistant pairs


@dataclass(frozen=True)
class ChatTurn:
    ts: float
    role: str  # "user" | "assistant"
    content: str


class SessionMemoryStore:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._sessions: dict[str, list[ChatTurn]] = {}

    def new_session_id(self) -> str:
        return uuid.uuid4().hex

    def add(self, session_id: str, role: str, content: str) -> None:
        content = (content or "").strip()
        if not session_id or not content:
            return
        role = role.strip().lower()
        if role not in ("user", "assistant"):
            return

        with self._lock:
            turns = self._sessions.setdefault(session_id, [])
            turns.append(ChatTurn(ts=time.time(), role=role, content=content))

            # Keep last N turns (pairs => 2 * N messages)
            max_msgs = max(2, 2 * _MAX_TURNS)
            if len(turns) > max_msgs:
                self._sessions[session_id] = turns[-max_msgs:]

    def get_context_text(self, session_id: str) -> str:
        if not session_id:
            return ""
        with self._lock:
            turns = list(self._sessions.get(session_id, []))
        if not turns:
            return ""
        lines: list[str] = []
        for t in turns:
            prefix = "User" if t.role == "user" else "Assistant"
            lines.append(f"{prefix}: {t.content}")
        return "\n".join(lines)


session_memory = SessionMemoryStore()

