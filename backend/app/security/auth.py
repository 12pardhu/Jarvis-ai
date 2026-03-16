from __future__ import annotations

import hmac
import os
from dataclasses import dataclass

import bcrypt


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def hash_secret(plain: str) -> str:
    plain_b = (plain or "").encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_b, salt).decode("utf-8")


def verify_secret(plain: str, hashed: str) -> bool:
    if not plain or not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


@dataclass(frozen=True)
class AuthConfig:
    api_token: str
    voice_hash: str
    pin_hash: str
    require_auth: bool


def get_auth_config() -> AuthConfig:
    # If REQUIRE_AUTH is false, auth endpoints still work but chat is open.
    require_auth = _env("JARVIS_REQUIRE_AUTH", "false").lower() == "true"
    return AuthConfig(
        api_token=_env("JARVIS_API_TOKEN", ""),
        voice_hash=_env("JARVIS_VOICE_PASSPHRASE_HASH", ""),
        pin_hash=_env("JARVIS_PIN_HASH", ""),
        require_auth=require_auth,
    )


def constant_time_equals(a: str, b: str) -> bool:
    return hmac.compare_digest((a or "").encode(), (b or "").encode())

