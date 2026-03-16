from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.security.auth import get_auth_config, verify_secret

router = APIRouter(prefix="/auth", tags=["auth"])


class VoiceLoginRequest(BaseModel):
    phrase: str


class PinLoginRequest(BaseModel):
    pin: str


@router.post("/voice")
def voice_login(body: VoiceLoginRequest):
    cfg = get_auth_config()
    if not cfg.voice_hash:
        raise HTTPException(status_code=500, detail="Voice auth not configured.")
    if verify_secret(body.phrase, cfg.voice_hash):
        return {"ok": True}
    raise HTTPException(status_code=401, detail="Invalid voice phrase.")


@router.post("/pin")
def pin_login(body: PinLoginRequest):
    cfg = get_auth_config()
    if not cfg.pin_hash:
        raise HTTPException(status_code=500, detail="PIN auth not configured.")
    if verify_secret(body.pin, cfg.pin_hash):
        return {"ok": True}
    raise HTTPException(status_code=401, detail="Invalid PIN.")

