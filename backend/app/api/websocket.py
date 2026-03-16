import os

from fastapi import APIRouter, WebSocket
from app.services.assistant_service import process_query
from app.memory.session_store import session_memory

router = APIRouter()

_WS_STREAMING = os.getenv("JARVIS_WS_STREAMING", "true").lower() == "true"

@router.websocket("/ws")

async def websocket_endpoint(ws: WebSocket):

    await ws.accept()
    session_id = session_memory.new_session_id()

    while True:

        msg = await ws.receive_text()

        # Instant response for automation is already handled at HTTP route level.
        # For WS, we focus on chat streaming UX.
        if not _WS_STREAMING:
            response = process_query(msg, session_id=session_id)
            await ws.send_text(response)
            continue

        # Minimal streaming protocol:
        # - send a "start" marker, then chunk the final text
        await ws.send_text("__jarvis_start__")
        response = process_query(msg, session_id=session_id)
        chunk_size = 180
        for i in range(0, len(response), chunk_size):
            await ws.send_text(response[i : i + chunk_size])
        await ws.send_text("__jarvis_end__")