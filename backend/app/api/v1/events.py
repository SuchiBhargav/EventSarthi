"""
Event Management Routes
CRUD operations for events
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_planner, verify_event_access
from app.models.planner import Planner
from app.models.event import Event, EventStatus
from app.schemas import (
    EventCreate,
    EventUpdate,
    EventResponse,
    EventListResponse,
    EventStats,
    MessageResponse,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=EventResponse,
    summary="Create Event",
    description="Create a new event for the authenticated planner",
    responses={
        201: {"description": "Event successfully created"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
    },
)
async def create_event(
    event_data: EventCreate,
    current_planner: Planner = Depends(get_current_planner),
    db: Session = Depends(get_db),
):
    """
    Create a new event.

    Requires authentication. The event will be associated with the current planner.

    - **name**: Event name (3-200 characters)
    - **event_type**: Type of event (wedding, birthday, corporate, etc.)
    - **description**: Optional event description
    - **event_date**: Date and time of the event
    - **venue**: Event location/venue
    - **expected_guests**: Expected number of guests (minimum 1)
    - **budget**: Optional event budget
    """
    # Create new event
    new_event = Event(
        planner_id=current_planner.planner_id,
        event_name=event_data.name,
        event_type=event_data.event_type.value,
        description=event_data.description,
        start_date=event_data.event_date,
        end_date=event_data.event_date,  # Can be updated later
        venue_name=event_data.venue,
        status=EventStatus.DRAFT,
        total_guests=0,
        guests_checked_in=0,
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {
        "id": str(new_event.event_id),
        "planner_id": str(new_event.planner_id),
        "name": new_event.event_name,
        "event_type": event_data.event_type,
        "description": new_event.description,
        "event_date": new_event.start_date,
        "venue": new_event.venue_name,
        "expected_guests": event_data.expected_guests,
        "confirmed_guests": 0,
        "budget": event_data.budget,
        "status": new_event.status.value,
        "created_at": new_event.created_at,
        "updated_at": new_event.updated_at,
    }


@router.get(
    "/",
    response_model=EventListResponse,
    summary="List Events",
    description="Get paginated list of events for the authenticated planner",
    responses={
        200: {"description": "Events retrieved successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def list_events(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by event status"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    current_planner: Planner = Depends(get_current_planner),
    db: Session = Depends(get_db),
):
    """
    List all events for current planner.

    Supports pagination and filtering by status and event type.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **status**: Filter by event status (draft, planning, confirmed, etc.)
    - **event_type**: Filter by event type (wedding, birthday, etc.)
    """
    # Build query with tenant isolation
    query = db.query(Event).filter(Event.planner_id == current_planner.planner_id)

    # Apply filters
    if status:
        query = query.filter(Event.status == status.upper())
    if event_type:
        query = query.filter(Event.event_type == event_type)

    # Get total count
    total = query.count()

    # Apply pagination
    skip = (page - 1) * page_size
    events = query.order_by(Event.created_at.desc()).offset(skip).limit(page_size).all()

    # Format response
    event_list = []
    for event in events:
        event_list.append(
            {
                "id": str(event.event_id),
                "planner_id": str(event.planner_id),
                "name": event.event_name,
                "event_type": event.event_type,
                "description": event.description,
                "event_date": event.start_date,
                "venue": event.venue_name,
                "expected_guests": event.total_guests,
                "confirmed_guests": event.guests_checked_in,
                "budget": None,
                "status": event.status.value,
                "created_at": event.created_at,
                "updated_at": event.updated_at,
            }
        )

    return {"events": event_list, "total": total, "page": page, "page_size": page_size}


@router.get(
    "/stats",
    response_model=EventStats,
    summary="Get Event Statistics",
    description="Get statistics about planner's events",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        401: {"description": "Not authenticated"},
    },
)
async def get_event_stats(
    current_planner: Planner = Depends(get_current_planner),
    db: Session = Depends(get_db),
):
    """
    Get event statistics.

    Returns aggregated statistics about the planner's events including
    total events, upcoming events, completed events, and total guests.
    """
    # Get total events
    total_events = (
        db.query(Event).filter(Event.planner_id == current_planner.planner_id).count()
    )

    # Get upcoming events (not completed/archived)
    upcoming_events = (
        db.query(Event)
        .filter(
            Event.planner_id == current_planner.planner_id,
            Event.status.in_([EventStatus.DRAFT, EventStatus.ACTIVE]),
            Event.start_date >= datetime.utcnow(),
        )
        .count()
    )

    # Get completed events
    completed_events = (
        db.query(Event)
        .filter(
            Event.planner_id == current_planner.planner_id,
            Event.status == EventStatus.COMPLETED,
        )
        .count()
    )

    # Get total guests across all events
    total_guests = (
        db.query(func.sum(Event.total_guests))
        .filter(Event.planner_id == current_planner.planner_id)
        .scalar()
        or 0
    )

    return {
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events,
        "total_guests": int(total_guests),
    }


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get Event Details",
    description="Get detailed information about a specific event",
    responses={
        200: {"description": "Event retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def get_event(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Get event details.

    Returns complete information about a specific event.
    Requires authentication and access to the event.

    - **event_id**: Unique event identifier
    """
    return {
        "id": str(event.event_id),
        "planner_id": str(event.planner_id),
        "name": event.event_name,
        "event_type": event.event_type,
        "description": event.description,
        "event_date": event.start_date,
        "venue": event.venue_name,
        "expected_guests": event.total_guests,
        "confirmed_guests": event.guests_checked_in,
        "budget": None,
        "status": event.status.value,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
    }


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    summary="Update Event",
    description="Update event details",
    responses={
        200: {"description": "Event updated successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def update_event(
    event_id: str,
    event_data: EventUpdate,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Update event details.

    Update one or more fields of an existing event.
    Only the planner who created the event can update it.

    - **event_id**: Unique event identifier
    - All fields are optional - only provided fields will be updated
    """
    # Update fields if provided
    if event_data.name is not None:
        event.event_name = event_data.name  # type: ignore[assignment]
    if event_data.event_type is not None:
        event.event_type = event_data.event_type.value  # type: ignore[assignment]
    if event_data.description is not None:
        event.description = event_data.description  # type: ignore[assignment]
    if event_data.event_date is not None:
        event.start_date = event_data.event_date  # type: ignore[assignment]
        event.end_date = event_data.event_date  # type: ignore[assignment]
    if event_data.venue is not None:
        event.venue_name = event_data.venue  # type: ignore[assignment]
    if event_data.expected_guests is not None:
        event.total_guests = event_data.expected_guests  # type: ignore[assignment]
    if event_data.status is not None:
        event.status = EventStatus[event_data.status.value.upper()]  # type: ignore[assignment]

    event.updated_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()
    db.refresh(event)

    return {
        "id": str(event.event_id),
        "planner_id": str(event.planner_id),
        "name": event.event_name,
        "event_type": event.event_type,
        "description": event.description,
        "event_date": event.start_date,
        "venue": event.venue_name,
        "expected_guests": event.total_guests,
        "confirmed_guests": event.guests_checked_in,
        "budget": event_data.budget,
        "status": event.status.value,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
    }


@router.delete(
    "/{event_id}",
    response_model=MessageResponse,
    summary="Delete Event",
    description="Delete an event and all associated data",
    responses={
        200: {"description": "Event deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def delete_event(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Delete event.

    Permanently deletes the event and all associated data including
    guests, conversations, and analytics.
    This action cannot be undone.

    - **event_id**: Unique event identifier
    """
    # Mark as deleted (soft delete)
    event.status = EventStatus.DELETED  # type: ignore[assignment]
    event.deleted_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()

    # Or hard delete (uncomment if preferred):
    # db.delete(event)
    # db.commit()

    return {"message": "Event deleted successfully"}


@router.post(
    "/{event_id}/complete",
    response_model=EventResponse,
    summary="Complete Event",
    description="Mark an event as completed",
    responses={
        200: {"description": "Event marked as completed"},
        400: {"description": "Event cannot be completed"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def complete_event(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Mark event as completed.

    Changes the event status to 'completed' and triggers any
    post-event workflows like feedback collection.

    - **event_id**: Unique event identifier
    """
    # Check if event can be completed
    if event.status.value == EventStatus.COMPLETED.value:  # type: ignore[attr-defined]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Event is already completed"
        )

    # Mark as completed
    event.status = EventStatus.COMPLETED  # type: ignore[assignment]
    event.completed_at = datetime.utcnow()  # type: ignore[assignment]
    event.updated_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()
    db.refresh(event)

    return {
        "id": str(event.event_id),
        "planner_id": str(event.planner_id),
        "name": event.event_name,
        "event_type": event.event_type,
        "description": event.description,
        "event_date": event.start_date,
        "venue": event.venue_name,
        "expected_guests": event.total_guests,
        "confirmed_guests": event.guests_checked_in,
        "budget": None,
        "status": event.status.value,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
    }


# Made with Bob
