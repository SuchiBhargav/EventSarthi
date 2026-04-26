"""Analytics Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/{event_id}/analytics")
async def get_event_analytics(event_id: str, db: Session = Depends(get_db)):
    """Get analytics for event"""
    return {"message": "Get analytics - to be implemented"}
