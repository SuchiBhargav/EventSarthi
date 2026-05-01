"""Conversation Routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import verify_event_access
from app.models.event import Event
from app.models.conversation import Conversation

router = APIRouter()


@router.get("/{event_id}/conversations")
async def list_conversations(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """List conversations for event"""
    conversations = (
        db.query(Conversation)
        .filter(Conversation.event_id == event.event_id)
        .order_by(Conversation.created_at.desc())
        .limit(50)
        .all()
    )

    return {
        "conversations": [
            {
                "conversation_id": str(conv.conversation_id),
                "guest_id": str(conv.guest_id),
                "event_id": str(conv.event_id),
                "last_message": conv.last_message,
                "last_message_at": conv.last_message_at,
                "created_at": conv.created_at,
            }
            for conv in conversations
        ],
        "total": len(conversations),
    }


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation details with messages"""
    conversation = (
        db.query(Conversation)
        .filter(Conversation.conversation_id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found"
        )

    return {
        "conversation_id": str(conversation.conversation_id),
        "guest_id": str(conversation.guest_id),
        "event_id": str(conversation.event_id),
        "messages": [],  # Would fetch from messages table
        "last_message": conversation.last_message,
        "last_message_at": conversation.last_message_at,
        "created_at": conversation.created_at,
    }
