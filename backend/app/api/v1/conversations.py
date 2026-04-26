"""Conversation Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/{event_id}/conversations")
async def list_conversations(event_id: str, db: Session = Depends(get_db)):
    """List conversations for event"""
    return {"message": "List conversations - to be implemented"}

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation details with messages"""
    return {"message": "Get conversation - to be implemented"}
