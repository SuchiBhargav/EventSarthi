"""
Guest Schemas
Pydantic models for guest requests and responses
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RSVPStatus(str, Enum):
    """RSVP status enumeration"""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    MAYBE = "maybe"


class GuestCreate(BaseModel):
    """Schema for creating a new guest"""

    name: str = Field(..., min_length=2, max_length=100, description="Guest name")
    phone_number: str = Field(..., description="Guest phone number with country code")
    email: Optional[EmailStr] = Field(None, description="Guest email address")
    plus_one: bool = Field(
        default=False, description="Whether guest can bring a plus one"
    )
    dietary_restrictions: Optional[str] = Field(
        None, description="Dietary restrictions or preferences"
    )
    notes: Optional[str] = Field(None, description="Additional notes about the guest")
    relation_type: Optional[str] = Field(
        default="other", description="Relationship to host/event family"
    )
    tone_preference: Optional[str] = Field(
        default="friendly", description="Preferred tone for personalized messages"
    )
    language: Optional[str] = Field(
        default="en", description="Preferred guest communication language"
    )
    vip_level: Optional[str] = Field(
        default="regular", description="Priority tier such as regular, vip, close"
    )
    food_preference: Optional[str] = Field(
        None, description="Food preference such as veg, non-veg, vegan, jain"
    )
    room_number: Optional[str] = Field(None, description="Assigned room number")
    hotel_name: Optional[str] = Field(None, description="Assigned hotel name")
    whatsapp_opted_in: Optional[bool] = Field(
        default=True, description="Whether WhatsApp communication is allowed"
    )
    notifications_enabled: Optional[bool] = Field(
        default=True, description="Whether scheduled notifications are enabled"
    )
    custom_fields: Optional[dict] = Field(
        default=None, description="Additional imported guest metadata"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Johnson",
                "phone_number": "+1234567890",
                "email": "alice@example.com",
                "plus_one": True,
                "dietary_restrictions": "Vegetarian",
                "notes": "Close friend of the bride",
                "relation_type": "friend",
                "tone_preference": "friendly",
                "language": "en",
                "vip_level": "vip",
                "food_preference": "veg",
                "room_number": "201",
                "hotel_name": "Grand Palace",
                "whatsapp_opted_in": True,
                "notifications_enabled": True,
                "custom_fields": {"priority": "high"},
            }
        }


class GuestUpdate(BaseModel):
    """Schema for updating a guest"""

    name: Optional[str] = Field(
        None, min_length=2, max_length=100, description="Guest name"
    )
    phone_number: Optional[str] = Field(None, description="Guest phone number")
    email: Optional[EmailStr] = Field(None, description="Guest email address")
    plus_one: Optional[bool] = Field(None, description="Plus one permission")
    dietary_restrictions: Optional[str] = Field(
        None, description="Dietary restrictions"
    )
    notes: Optional[str] = Field(None, description="Additional notes")
    relation_type: Optional[str] = Field(None, description="Relationship to host")
    tone_preference: Optional[str] = Field(
        None, description="Preferred tone for personalized messages"
    )
    language: Optional[str] = Field(None, description="Preferred language")
    vip_level: Optional[str] = Field(None, description="Priority tier")
    food_preference: Optional[str] = Field(None, description="Food preference")
    room_number: Optional[str] = Field(None, description="Room number")
    hotel_name: Optional[str] = Field(None, description="Hotel name")
    whatsapp_opted_in: Optional[bool] = Field(
        None, description="Whether WhatsApp communication is allowed"
    )
    notifications_enabled: Optional[bool] = Field(
        None, description="Whether scheduled notifications are enabled"
    )
    custom_fields: Optional[dict] = Field(
        None, description="Additional imported guest metadata"
    )
    rsvp_status: Optional[RSVPStatus] = Field(None, description="RSVP status")

    class Config:
        json_schema_extra = {
            "example": {
                "rsvp_status": "confirmed",
                "dietary_restrictions": "Vegan",
                "relation_type": "family",
                "vip_level": "vip",
            }
        }


class GuestResponse(BaseModel):
    """Schema for guest response"""

    id: str = Field(..., description="Guest unique identifier")
    event_id: str = Field(..., description="Associated event ID")
    name: str = Field(..., description="Guest name")
    phone_number: str = Field(..., description="Guest phone number")
    email: Optional[EmailStr] = Field(None, description="Guest email address")
    plus_one: bool = Field(..., description="Plus one permission")
    dietary_restrictions: Optional[str] = Field(
        None, description="Dietary restrictions"
    )
    notes: Optional[str] = Field(None, description="Additional notes")
    relation_type: Optional[str] = Field(None, description="Relationship to host")
    tone_preference: Optional[str] = Field(
        None, description="Preferred tone for personalized messages"
    )
    language: Optional[str] = Field(None, description="Preferred language")
    vip_level: Optional[str] = Field(None, description="Priority tier")
    food_preference: Optional[str] = Field(None, description="Food preference")
    room_number: Optional[str] = Field(None, description="Room number")
    hotel_name: Optional[str] = Field(None, description="Hotel name")
    whatsapp_opted_in: bool = Field(..., description="WhatsApp opt-in flag")
    notifications_enabled: bool = Field(..., description="Notification opt-in flag")
    custom_fields: Optional[dict] = Field(
        None, description="Additional imported guest metadata"
    )
    rsvp_status: RSVPStatus = Field(..., description="RSVP status")
    rsvp_date: Optional[datetime] = Field(
        None, description="Date when RSVP was received"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "guest_123abc",
                "event_id": "event_456def",
                "name": "Alice Johnson",
                "phone_number": "+1234567890",
                "email": "alice@example.com",
                "plus_one": True,
                "dietary_restrictions": "Vegetarian",
                "notes": "Close friend of the bride",
                "relation_type": "friend",
                "tone_preference": "friendly",
                "language": "en",
                "vip_level": "vip",
                "food_preference": "veg",
                "room_number": "201",
                "hotel_name": "Grand Palace",
                "whatsapp_opted_in": True,
                "notifications_enabled": True,
                "custom_fields": {"priority": "high"},
                "rsvp_status": "confirmed",
                "rsvp_date": "2024-02-15T10:30:00Z",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-02-15T10:30:00Z",
            }
        }


class GuestListResponse(BaseModel):
    """Schema for paginated guest list response"""

    guests: List[GuestResponse] = Field(..., description="List of guests")
    total: int = Field(..., description="Total number of guests")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")

    class Config:
        json_schema_extra = {
            "example": {
                "guests": [
                    {
                        "id": "guest_123abc",
                        "event_id": "event_456def",
                        "name": "Alice Johnson",
                        "phone_number": "+1234567890",
                        "email": "alice@example.com",
                        "rsvp_status": "confirmed",
                        "created_at": "2024-01-15T10:30:00Z",
                    }
                ],
                "total": 150,
                "page": 1,
                "page_size": 20,
            }
        }


class GuestStats(BaseModel):
    """Schema for guest statistics"""

    total_guests: int = Field(..., description="Total number of guests")
    confirmed: int = Field(..., description="Number of confirmed guests")
    declined: int = Field(..., description="Number of declined guests")
    pending: int = Field(..., description="Number of pending responses")
    maybe: int = Field(..., description="Number of maybe responses")

    class Config:
        json_schema_extra = {
            "example": {
                "total_guests": 150,
                "confirmed": 120,
                "declined": 10,
                "pending": 15,
                "maybe": 5,
            }
        }


class BulkGuestImport(BaseModel):
    """Schema for bulk guest import"""

    guests: List[GuestCreate] = Field(..., description="List of guests to import")

    class Config:
        json_schema_extra = {
            "example": {
                "guests": [
                    {
                        "name": "Alice Johnson",
                        "phone_number": "+1234567890",
                        "email": "alice@example.com",
                    },
                    {
                        "name": "Bob Smith",
                        "phone_number": "+1234567891",
                        "email": "bob@example.com",
                    },
                ]
            }
        }


# Made with Bob
