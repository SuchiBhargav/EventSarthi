"""Support Request Routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.dependencies import verify_event_access
from app.models.event import Event
from app.models.support_request import SupportRequest

router = APIRouter()


class SupportRequestUpdate(BaseModel):
    """Schema for updating support request"""

    status: str


class SupportRequestReply(BaseModel):
    """Schema for replying to support request"""

    reply_message: str


@router.get("/{event_id}/support-requests")
async def list_support_requests(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """List support requests for event"""
    requests = (
        db.query(SupportRequest)
        .filter(SupportRequest.event_id == event.event_id)
        .order_by(SupportRequest.created_at.desc())
        .all()
    )

    return {
        "support_requests": [
            {
                "request_id": str(req.request_id),
                "guest_id": str(req.guest_id),
                "subject": req.subject,
                "message": req.message,
                "status": req.status,
                "priority": req.priority,
                "created_at": req.created_at,
                "resolved_at": req.resolved_at,
            }
            for req in requests
        ],
        "total": len(requests),
    }


@router.put("/support-requests/{request_id}")
async def update_support_request(
    request_id: str, update_data: SupportRequestUpdate, db: Session = Depends(get_db)
):
    """Update support request status"""
    support_request = (
        db.query(SupportRequest).filter(SupportRequest.request_id == request_id).first()
    )

    if not support_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Support request not found"
        )

    support_request.status = update_data.status  # type: ignore[assignment]
    if update_data.status == "resolved":
        support_request.resolved_at = datetime.utcnow()  # type: ignore[assignment]

    db.commit()
    db.refresh(support_request)

    return {
        "request_id": str(support_request.request_id),
        "status": support_request.status,
        "resolved_at": support_request.resolved_at,
    }


@router.post("/support-requests/{request_id}/reply")
async def reply_to_support_request(
    request_id: str, reply_data: SupportRequestReply, db: Session = Depends(get_db)
):
    """Reply to guest support request"""
    support_request = (
        db.query(SupportRequest).filter(SupportRequest.request_id == request_id).first()
    )

    if not support_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Support request not found"
        )

    # In production, send reply via WhatsApp
    # For now, just update the request
    support_request.status = "replied"  # type: ignore[assignment]
    support_request.updated_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()

    return {
        "message": "Reply sent successfully",
        "request_id": str(support_request.request_id),
    }
