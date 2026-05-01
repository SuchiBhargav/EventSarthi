"""Broadcast Routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.dependencies import verify_event_access
from app.models.event import Event
from app.models.broadcast import Broadcast

router = APIRouter()


class BroadcastCreate(BaseModel):
    """Schema for creating broadcast"""

    message: str
    send_immediately: bool = True


@router.post("/{event_id}/broadcasts")
async def create_broadcast(
    event_id: str,
    broadcast_data: BroadcastCreate,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """Create and send broadcast message"""
    new_broadcast = Broadcast(
        event_id=event.event_id,
        planner_id=event.planner_id,
        message=broadcast_data.message,
        status="pending" if not broadcast_data.send_immediately else "sent",
        sent_at=datetime.utcnow() if broadcast_data.send_immediately else None,
    )

    db.add(new_broadcast)
    db.commit()
    db.refresh(new_broadcast)

    return {
        "broadcast_id": str(new_broadcast.broadcast_id),
        "message": broadcast_data.message,
        "status": new_broadcast.status,
        "created_at": new_broadcast.created_at,
        "sent_at": new_broadcast.sent_at,
    }


@router.get("/{event_id}/broadcasts")
async def list_broadcasts(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """List all broadcasts for event"""
    broadcasts = (
        db.query(Broadcast)
        .filter(Broadcast.event_id == event.event_id)
        .order_by(Broadcast.created_at.desc())
        .all()
    )

    return {
        "broadcasts": [
            {
                "broadcast_id": str(b.broadcast_id),
                "message": b.message,
                "status": b.status,
                "created_at": b.created_at,
                "sent_at": b.sent_at,
            }
            for b in broadcasts
        ],
        "total": len(broadcasts),
    }
