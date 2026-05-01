"""Analytics Routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import verify_event_access
from app.models.event import Event
from app.models.guest import Guest
from app.models.conversation import Conversation
from app.models.broadcast import Broadcast

router = APIRouter()


@router.get("/{event_id}/analytics")
async def get_event_analytics(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """Get analytics for event"""
    # Guest statistics
    total_guests = db.query(Guest).filter(Guest.event_id == event.event_id).count()
    confirmed_guests = (
        db.query(Guest)
        .filter(Guest.event_id == event.event_id, Guest.is_attending)
        .count()
    )
    checked_in_guests = (
        db.query(Guest)
        .filter(Guest.event_id == event.event_id, Guest.checked_in)
        .count()
    )

    # Conversation statistics
    total_conversations = (
        db.query(Conversation).filter(Conversation.event_id == event.event_id).count()
    )

    # Broadcast statistics
    total_broadcasts = (
        db.query(Broadcast).filter(Broadcast.event_id == event.event_id).count()
    )

    return {
        "event_id": str(event.event_id),
        "event_name": event.event_name,
        "guest_analytics": {
            "total_guests": total_guests,
            "confirmed_guests": confirmed_guests,
            "checked_in_guests": checked_in_guests,
            "attendance_rate": round(
                (confirmed_guests / total_guests * 100) if total_guests > 0 else 0, 2
            ),
        },
        "engagement_analytics": {
            "total_conversations": total_conversations,
            "total_broadcasts": total_broadcasts,
        },
        "event_status": event.status.value,
        "created_at": event.created_at,
    }
