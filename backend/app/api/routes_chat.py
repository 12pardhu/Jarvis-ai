from fastapi import APIRouter
from pydantic import BaseModel
from app.services.assistant_service import process_query

router = APIRouter(prefix="/chat")

class ChatRequest(BaseModel):
    query: str

@router.post("/")
def chat(body: ChatRequest):
    response = process_query(body.query)
    return {"response": response}