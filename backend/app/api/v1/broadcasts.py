"""Broadcast Routes"""

from typing import Optional, Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime
from app.database import get_db
from app.dependencies import verify_event_access
from app.models.event import Event
from app.models.broadcast import Broadcast, BroadcastStatus
from app.models.guest import Guest

router = APIRouter()


class BroadcastCreate(BaseModel):
    """Schema for creating broadcast"""

    message: str = Field(
        ...,
        description="Message template. Supports placeholders like {{name}}, {{relation_type}}, {{vip_level}}",
    )
    send_immediately: bool = True
    scheduled_at: Optional[datetime] = None
    use_personalization: bool = True
    target_filter: Optional[Dict[str, Any]] = None


def _build_guest_query(db: Session, event: Event, target_filter: Optional[Dict[str, Any]]):
    query = db.query(Guest).filter(
        Guest.event_id == event.event_id,
        Guest.whatsapp_opted_in.is_(True),
        Guest.notifications_enabled.is_(True),
    )

    if not target_filter:
        return query

    relation_type = target_filter.get("relation_type")
    vip_level = target_filter.get("vip_level")
    language = target_filter.get("language")
    hotel_name = target_filter.get("hotel_name")
    room_number = target_filter.get("room_number")

    if relation_type:
        query = query.filter(Guest.relation_type == relation_type)
    if vip_level:
        query = query.filter(Guest.vip_level == vip_level)
    if language:
        query = query.filter(Guest.language == language)
    if hotel_name:
        query = query.filter(Guest.hotel_name == hotel_name)
    if room_number:
        query = query.filter(Guest.room_number == room_number)

    return query


@router.post("/{event_id}/broadcasts")
async def create_broadcast(
    event_id: str,
    broadcast_data: BroadcastCreate,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """Create broadcast message or scheduled personalized broadcast"""
    recipients_query = _build_guest_query(db, event, broadcast_data.target_filter)
    total_recipients = recipients_query.count()

    is_scheduled = (
        not broadcast_data.send_immediately
        or broadcast_data.scheduled_at is not None
    )

    new_broadcast = Broadcast(
        event_id=event.event_id,
        planner_id=event.planner_id,
        message=broadcast_data.message,
        status=BroadcastStatus.SCHEDULED if is_scheduled else BroadcastStatus.SENT,
        scheduled_at=broadcast_data.scheduled_at,
        use_personalization=broadcast_data.use_personalization,
        target_filter=broadcast_data.target_filter,
        total_recipients=total_recipients,
        sent_count=total_recipients if not is_scheduled else 0,
        started_at=datetime.utcnow() if not is_scheduled else None,
        completed_at=datetime.utcnow() if not is_scheduled else None,
    )

    db.add(new_broadcast)
    db.commit()
    db.refresh(new_broadcast)

    return {
        "broadcast_id": str(new_broadcast.broadcast_id),
        "message": new_broadcast.message,
        "status": new_broadcast.status.value
        if new_broadcast.status is not None
        else None,
        "scheduled_at": new_broadcast.scheduled_at,
        "use_personalization": new_broadcast.use_personalization,
        "target_filter": new_broadcast.target_filter,
        "total_recipients": new_broadcast.total_recipients,
        "template_variables": ["{{name}}", "{{relation_type}}", "{{vip_level}}"],
        "created_at": new_broadcast.created_at,
        "started_at": new_broadcast.started_at,
        "completed_at": new_broadcast.completed_at,
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
                "status": b.status.value if b.status is not None else None,
                "scheduled_at": b.scheduled_at,
                "use_personalization": b.use_personalization,
                "target_filter": b.target_filter,
                "total_recipients": b.total_recipients,
                "sent_count": b.sent_count,
                "delivered_count": b.delivered_count,
                "failed_count": b.failed_count,
                "created_at": b.created_at,
                "started_at": b.started_at,
                "completed_at": b.completed_at,
            }
            for b in broadcasts
        ],
        "total": len(broadcasts),
    }
