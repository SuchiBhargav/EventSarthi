"""
Guest Management Routes
CRUD operations for event guests
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.dependencies import verify_event_access
from app.models.event import Event
from app.models.guest import Guest
from app.schemas import (
    GuestCreate,
    GuestUpdate,
    GuestResponse,
    GuestListResponse,
    GuestStats,
    BulkGuestImport,
    MessageResponse,
    RSVPStatus,
)

router = APIRouter()


@router.post(
    "/{event_id}/guests",
    status_code=status.HTTP_201_CREATED,
    response_model=GuestResponse,
    summary="Add Guest",
    description="Add a new guest to an event",
    responses={
        201: {"description": "Guest successfully added"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def add_guest(
    event_id: str,
    guest_data: GuestCreate,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Add a guest to an event.

    Creates a new guest entry for the specified event.

    - **event_id**: Event identifier
    - **name**: Guest name (2-100 characters)
    - **phone_number**: Phone number with country code
    - **email**: Optional email address
    - **plus_one**: Whether guest can bring a plus one
    - **dietary_restrictions**: Optional dietary preferences
    - **notes**: Optional additional notes
    """
    # Check if guest with same phone already exists for this event
    existing_guest = (
        db.query(Guest)
        .filter(
            Guest.event_id == event.event_id, Guest.phone == guest_data.phone_number
        )
        .first()
    )

    if existing_guest:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Guest with this phone number already exists for this event",
        )

    # Create new guest
    new_guest = Guest(
        event_id=event.event_id,
        planner_id=event.planner_id,
        name=guest_data.name,
        phone=guest_data.phone_number,
        email=guest_data.email,
        plus_ones=1 if guest_data.plus_one else 0,
        dietary_restrictions=guest_data.dietary_restrictions,
        notes=guest_data.notes,
        is_attending=True,
        checked_in=False,
    )

    db.add(new_guest)

    # Update event guest count
    event.total_guests = (  # type: ignore[assignment]
        db.query(Guest).filter(Guest.event_id == event.event_id).count() + 1
    )

    db.commit()
    db.refresh(new_guest)

    return {
        "id": str(new_guest.guest_id),
        "event_id": str(new_guest.event_id),
        "name": new_guest.name,
        "phone_number": new_guest.phone,
        "email": new_guest.email,
        "plus_one": new_guest.plus_ones > 0,
        "dietary_restrictions": new_guest.dietary_restrictions,
        "notes": new_guest.notes,
        "rsvp_status": RSVPStatus.PENDING,
        "rsvp_date": None,
        "created_at": new_guest.created_at,
        "updated_at": new_guest.updated_at,
    }


@router.get(
    "/{event_id}/guests",
    response_model=GuestListResponse,
    summary="List Guests",
    description="Get paginated list of guests for an event",
    responses={
        200: {"description": "Guests retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def list_guests(
    event_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    rsvp_status: Optional[str] = Query(None, description="Filter by RSVP status"),
    search: Optional[str] = Query(None, description="Search by name or phone"),
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    List all guests for an event.

    Supports pagination, filtering by RSVP status, and search.

    - **event_id**: Event identifier
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **rsvp_status**: Filter by RSVP status (pending, confirmed, declined, maybe)
    - **search**: Search guests by name or phone number
    """
    # Build query
    query = db.query(Guest).filter(Guest.event_id == event.event_id)

    # Apply search filter
    if search:
        query = query.filter(
            or_(Guest.name.ilike(f"%{search}%"), Guest.phone.ilike(f"%{search}%"))
        )

    # Get total count
    total = query.count()

    # Apply pagination
    skip = (page - 1) * page_size
    guests = query.order_by(Guest.created_at.desc()).offset(skip).limit(page_size).all()

    # Format response
    guest_list = []
    for guest in guests:
        is_attending = guest.is_attending is True
        guest_list.append(
            {
                "id": str(guest.guest_id),
                "event_id": str(guest.event_id),
                "name": guest.name,
                "phone_number": guest.phone,
                "email": guest.email,
                "plus_one": guest.plus_ones > 0,
                "dietary_restrictions": guest.dietary_restrictions,
                "notes": guest.notes,
                "rsvp_status": RSVPStatus.CONFIRMED
                if is_attending
                else RSVPStatus.PENDING,
                "rsvp_date": guest.updated_at if is_attending else None,
                "created_at": guest.created_at,
                "updated_at": guest.updated_at,
            }
        )

    return {"guests": guest_list, "total": total, "page": page, "page_size": page_size}


@router.get(
    "/{event_id}/guests/stats",
    response_model=GuestStats,
    summary="Get Guest Statistics",
    description="Get RSVP statistics for an event",
    responses={
        200: {"description": "Statistics retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def get_guest_stats(
    event_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Get guest statistics.

    Returns aggregated RSVP statistics including total guests,
    confirmed, declined, pending, and maybe responses.

    - **event_id**: Event identifier
    """
    total_guests = db.query(Guest).filter(Guest.event_id == event.event_id).count()

    confirmed = (
        db.query(Guest)
        .filter(Guest.event_id == event.event_id, Guest.is_attending)
        .count()
    )
    
    declined = (
        db.query(Guest)
        .filter(Guest.event_id == event.event_id, ~Guest.is_attending)
        .count()
    )

    pending = total_guests - confirmed - declined

    return {
        "total_guests": total_guests,
        "confirmed": confirmed,
        "declined": declined,
        "pending": pending,
        "maybe": 0,
    }


@router.get(
    "/{event_id}/guests/{guest_id}",
    response_model=GuestResponse,
    summary="Get Guest Details",
    description="Get detailed information about a specific guest",
    responses={
        200: {"description": "Guest retrieved successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Guest or event not found"},
    },
)
async def get_guest(
    event_id: str,
    guest_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Get guest details.

    Returns complete information about a specific guest.

    - **event_id**: Event identifier
    - **guest_id**: Guest identifier
    """
    guest = (
        db.query(Guest)
        .filter(Guest.guest_id == guest_id, Guest.event_id == event.event_id)
        .first()
    )

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )

    is_attending = guest.is_attending is True
    return {
        "id": str(guest.guest_id),
        "event_id": str(guest.event_id),
        "name": guest.name,
        "phone_number": guest.phone,
        "email": guest.email,
        "plus_one": guest.plus_ones > 0,
        "dietary_restrictions": guest.dietary_restrictions,
        "notes": guest.notes,
        "rsvp_status": RSVPStatus.CONFIRMED if is_attending else RSVPStatus.PENDING,
        "rsvp_date": guest.updated_at if is_attending else None,
        "created_at": guest.created_at,
        "updated_at": guest.updated_at,
    }


@router.put(
    "/{event_id}/guests/{guest_id}",
    response_model=GuestResponse,
    summary="Update Guest",
    description="Update guest details",
    responses={
        200: {"description": "Guest updated successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Guest or event not found"},
    },
)
async def update_guest(
    event_id: str,
    guest_id: str,
    guest_data: GuestUpdate,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Update guest details.

    Update one or more fields of an existing guest.
    All fields are optional - only provided fields will be updated.

    - **event_id**: Event identifier
    - **guest_id**: Guest identifier
    """
    guest = (
        db.query(Guest)
        .filter(Guest.guest_id == guest_id, Guest.event_id == event.event_id)
        .first()
    )

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )

    # Update fields if provided
    if guest_data.name is not None:
        guest.name = guest_data.name  # type: ignore[assignment]
    if guest_data.phone_number is not None:
        guest.phone = guest_data.phone_number  # type: ignore[assignment]
    if guest_data.email is not None:
        guest.email = guest_data.email  # type: ignore[assignment]
    if guest_data.plus_one is not None:
        guest.plus_ones = 1 if guest_data.plus_one else 0  # type: ignore[assignment]
    if guest_data.dietary_restrictions is not None:
        guest.dietary_restrictions = guest_data.dietary_restrictions  # type: ignore[assignment]
    if guest_data.notes is not None:
        guest.notes = guest_data.notes  # type: ignore[assignment]
    if guest_data.rsvp_status is not None:
        guest.is_attending = guest_data.rsvp_status == RSVPStatus.CONFIRMED  # type: ignore[assignment]

    guest.updated_at = datetime.utcnow()  # type: ignore[assignment]
    db.commit()
    db.refresh(guest)

    is_attending = guest.is_attending is True
    return {
        "id": str(guest.guest_id),
        "event_id": str(guest.event_id),
        "name": guest.name,
        "phone_number": guest.phone,
        "email": guest.email,
        "plus_one": guest.plus_ones > 0,
        "dietary_restrictions": guest.dietary_restrictions,
        "notes": guest.notes,
        "rsvp_status": RSVPStatus.CONFIRMED if is_attending else RSVPStatus.PENDING,
        "rsvp_date": guest.updated_at if is_attending else None,
        "created_at": guest.created_at,
        "updated_at": guest.updated_at,
    }


@router.delete(
    "/{event_id}/guests/{guest_id}",
    response_model=MessageResponse,
    summary="Delete Guest",
    description="Remove a guest from an event",
    responses={
        200: {"description": "Guest deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Guest or event not found"},
    },
)
async def delete_guest(
    event_id: str,
    guest_id: str,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Delete a guest.

    Permanently removes the guest from the event.
    This action cannot be undone.

    - **event_id**: Event identifier
    - **guest_id**: Guest identifier
    """
    guest = (
        db.query(Guest)
        .filter(Guest.guest_id == guest_id, Guest.event_id == event.event_id)
        .first()
    )

    if not guest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Guest not found"
        )

    db.delete(guest)

    # Update event guest count
    event.total_guests = (  # type: ignore[assignment]
        db.query(Guest).filter(Guest.event_id == event.event_id).count() - 1
    )

    db.commit()

    return {"message": "Guest deleted successfully"}


@router.post(
    "/{event_id}/guests/import",
    response_model=MessageResponse,
    summary="Bulk Import Guests",
    description="Import multiple guests at once",
    responses={
        200: {"description": "Guests imported successfully"},
        400: {"description": "Invalid input data"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied to this event"},
        404: {"description": "Event not found"},
    },
)
async def import_guests(
    event_id: str,
    import_data: BulkGuestImport,
    event: Event = Depends(verify_event_access),
    db: Session = Depends(get_db),
):
    """
    Bulk import guests.

    Import multiple guests at once from a list.
    Useful for importing from CSV/Excel files.

    - **event_id**: Event identifier
    - **guests**: List of guest data to import
    """
    imported_count = 0
    skipped_count = 0

    for guest_data in import_data.guests:
        # Check if guest already exists
        existing = (
            db.query(Guest)
            .filter(
                Guest.event_id == event.event_id, Guest.phone == guest_data.phone_number
            )
            .first()
        )

        if existing:
            skipped_count += 1
            continue

        # Create new guest
        new_guest = Guest(
            event_id=event.event_id,
            planner_id=event.planner_id,
            name=guest_data.name,
            phone=guest_data.phone_number,
            email=guest_data.email,
            plus_ones=1 if guest_data.plus_one else 0,
            dietary_restrictions=guest_data.dietary_restrictions,
            notes=guest_data.notes,
            is_attending=True,
            checked_in=False,
        )

        db.add(new_guest)
        imported_count += 1

    # Update event guest count
    event.total_guests = (  # type: ignore[assignment]
        db.query(Guest).filter(Guest.event_id == event.event_id).count()
        + imported_count
    )

    db.commit()

    return {
        "message": f"Successfully imported {imported_count} guests. Skipped {skipped_count} duplicates."
    }


# Made with Bob
