from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.voice.offline_voice import listen_offline
from app.api.routes_chat import router as chat_router
from app.router.command_router import route_command
from app.memory.session_store import session_memory
from app.security.auth import verify_secret, get_auth_config
from app.memory.session_store import session_memory

# 🚀 Initialize app
app = FastAPI(title="Jarvis AI")

# 🌐 Enable CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📡 Include chat routes
app.include_router(chat_router)

# 🏠 Root endpoint
@app.get("/")
def root():
    return {"message": "Jarvis AI is running 🚀"}

# 🔒 Auth endpoints
class VoiceAuthRequest(BaseModel):
    phrase: str

class PinAuthRequest(BaseModel):
    pin: str

@app.post("/auth/voice")
def auth_voice(body: VoiceAuthRequest):
    cfg = get_auth_config()
    if not cfg.voice_hash:
        return {"status": "ok", "message": "Voice auth not configured"}
    if verify_secret(body.phrase.lower().strip(), cfg.voice_hash):
        return {"status": "ok"}
    raise HTTPException(status_code=401, detail="Invalid phrase")

@app.post("/auth/pin")
def auth_pin(body: PinAuthRequest):
    cfg = get_auth_config()
    if not cfg.pin_hash:
        return {"status": "ok", "message": "PIN auth not configured"}
    if verify_secret(body.pin.strip(), cfg.pin_hash):
        return {"status": "ok"}
    raise HTTPException(status_code=401, detail="Invalid PIN")

# 📦 Request model
class JarvisChatRequest(BaseModel):
    message: str = ""
    session_id: Optional[str] = None

# 🤖 Main Jarvis endpoint
@app.post("/jarvis-chat")
def jarvis_chat(body: JarvisChatRequest):

    # 🔑 Create or reuse session
    sid = body.session_id or session_memory.new_session_id()

    # 🧠 Route command (automation + AI)
    response = route_command(body.message or "", session_id=sid)

    return {
        "response": response,
        "session_id": sid
    }

@app.get("/offline-voice")
def offline_voice():
    command = listen_offline()
    response = route_command(command)
    return {"command": command, "response": response}