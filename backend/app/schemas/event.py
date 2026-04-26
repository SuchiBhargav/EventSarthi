"""
Event Schemas
Pydantic models for event requests and responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Event type enumeration"""
    WEDDING = "wedding"
    BIRTHDAY = "birthday"
    CORPORATE = "corporate"
    CONFERENCE = "conference"
    PARTY = "party"
    OTHER = "other"


class EventStatus(str, Enum):
    """Event status enumeration"""
    DRAFT = "draft"
    PLANNING = "planning"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EventCreate(BaseModel):
    """Schema for creating a new event"""
    name: str = Field(..., min_length=3, max_length=200, description="Event name")
    event_type: EventType = Field(..., description="Type of event")
    description: Optional[str] = Field(None, description="Event description")
    event_date: datetime = Field(..., description="Event date and time")
    venue: str = Field(..., description="Event venue/location")
    expected_guests: int = Field(..., ge=1, description="Expected number of guests")
    budget: Optional[float] = Field(None, ge=0, description="Event budget")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John & Jane's Wedding",
                "event_type": "wedding",
                "description": "A beautiful outdoor wedding ceremony",
                "event_date": "2024-06-15T14:00:00Z",
                "venue": "Grand Hotel Ballroom, New York",
                "expected_guests": 150,
                "budget": 50000.00
            }
        }


class EventUpdate(BaseModel):
    """Schema for updating an event"""
    name: Optional[str] = Field(None, min_length=3, max_length=200, description="Event name")
    event_type: Optional[EventType] = Field(None, description="Type of event")
    description: Optional[str] = Field(None, description="Event description")
    event_date: Optional[datetime] = Field(None, description="Event date and time")
    venue: Optional[str] = Field(None, description="Event venue/location")
    expected_guests: Optional[int] = Field(None, ge=1, description="Expected number of guests")
    budget: Optional[float] = Field(None, ge=0, description="Event budget")
    status: Optional[EventStatus] = Field(None, description="Event status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "John & Jane's Wedding - Updated",
                "expected_guests": 175,
                "status": "confirmed"
            }
        }


class EventResponse(BaseModel):
    """Schema for event response"""
    id: str = Field(..., description="Event unique identifier")
    planner_id: str = Field(..., description="Planner ID who created the event")
    name: str = Field(..., description="Event name")
    event_type: EventType = Field(..., description="Type of event")
    description: Optional[str] = Field(None, description="Event description")
    event_date: datetime = Field(..., description="Event date and time")
    venue: str = Field(..., description="Event venue/location")
    expected_guests: int = Field(..., description="Expected number of guests")
    confirmed_guests: int = Field(default=0, description="Number of confirmed guests")
    budget: Optional[float] = Field(None, description="Event budget")
    status: EventStatus = Field(..., description="Event status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "event_123abc",
                "planner_id": "planner_456def",
                "name": "John & Jane's Wedding",
                "event_type": "wedding",
                "description": "A beautiful outdoor wedding ceremony",
                "event_date": "2024-06-15T14:00:00Z",
                "venue": "Grand Hotel Ballroom, New York",
                "expected_guests": 150,
                "confirmed_guests": 120,
                "budget": 50000.00,
                "status": "confirmed",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-02-20T15:45:00Z"
            }
        }


class EventListResponse(BaseModel):
    """Schema for paginated event list response"""
    events: List[EventResponse] = Field(..., description="List of events")
    total: int = Field(..., description="Total number of events")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "events": [
                    {
                        "id": "event_123abc",
                        "planner_id": "planner_456def",
                        "name": "John & Jane's Wedding",
                        "event_type": "wedding",
                        "event_date": "2024-06-15T14:00:00Z",
                        "venue": "Grand Hotel Ballroom",
                        "expected_guests": 150,
                        "confirmed_guests": 120,
                        "status": "confirmed",
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-02-20T15:45:00Z"
                    }
                ],
                "total": 25,
                "page": 1,
                "page_size": 20
            }
        }


class EventStats(BaseModel):
    """Schema for event statistics"""
    total_events: int = Field(..., description="Total number of events")
    upcoming_events: int = Field(..., description="Number of upcoming events")
    completed_events: int = Field(..., description="Number of completed events")
    total_guests: int = Field(..., description="Total guests across all events")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_events": 25,
                "upcoming_events": 10,
                "completed_events": 15,
                "total_guests": 3500
            }
        }

# Made with Bob