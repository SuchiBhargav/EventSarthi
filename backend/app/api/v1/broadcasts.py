"""Broadcast Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/{event_id}/broadcasts")
async def create_broadcast(event_id: str, db: Session = Depends(get_db)):
    """Create and send broadcast message"""
    return {"message": "Create broadcast - to be implemented"}

@router.get("/{event_id}/broadcasts")
async def list_broadcasts(event_id: str, db: Session = Depends(get_db)):
    """List all broadcasts for event"""
    return {"message": "List broadcasts - to be implemented"}
