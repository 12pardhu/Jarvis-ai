from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.voice.offline_voice import listen_offline
# 🔥 Core imports (keep only stable ones)
from app.api.routes_chat import router as chat_router
from app.router.command_router import route_command
from app.memory.session_store import session_memory

# 🚀 Initialize app
app = FastAPI(title="Jarvis AI")

# 🌐 Enable CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📡 Include chat routes
app.include_router(chat_router)

# 🏠 Root endpoint
@app.get("/")
def root():
    return {"message": "Jarvis AI is running 🚀"}

# 📦 Request model
class JarvisChatRequest(BaseModel):
    message: str = ""
    session_id: str | None = None

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