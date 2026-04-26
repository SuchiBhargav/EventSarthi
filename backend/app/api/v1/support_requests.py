"""Support Request Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/{event_id}/support-requests")
async def list_support_requests(event_id: str, db: Session = Depends(get_db)):
    """List support requests for event"""
    return {"message": "List support requests - to be implemented"}

@router.put("/support-requests/{request_id}")
async def update_support_request(request_id: str, db: Session = Depends(get_db)):
    """Update support request status"""
    return {"message": "Update support request - to be implemented"}

@router.post("/support-requests/{request_id}/reply")
async def reply_to_support_request(request_id: str, db: Session = Depends(get_db)):
    """Reply to guest support request"""
    return {"message": "Reply to support request - to be implemented"}
