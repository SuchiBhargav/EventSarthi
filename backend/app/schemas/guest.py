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
    plus_one: bool = Field(default=False, description="Whether guest can bring a plus one")
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions or preferences")
    notes: Optional[str] = Field(None, description="Additional notes about the guest")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Johnson",
                "phone_number": "+1234567890",
                "email": "alice@example.com",
                "plus_one": True,
                "dietary_restrictions": "Vegetarian",
                "notes": "Close friend of the bride"
            }
        }


class GuestUpdate(BaseModel):
    """Schema for updating a guest"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Guest name")
    phone_number: Optional[str] = Field(None, description="Guest phone number")
    email: Optional[EmailStr] = Field(None, description="Guest email address")
    plus_one: Optional[bool] = Field(None, description="Plus one permission")
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions")
    notes: Optional[str] = Field(None, description="Additional notes")
    rsvp_status: Optional[RSVPStatus] = Field(None, description="RSVP status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rsvp_status": "confirmed",
                "dietary_restrictions": "Vegan"
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
    dietary_restrictions: Optional[str] = Field(None, description="Dietary restrictions")
    notes: Optional[str] = Field(None, description="Additional notes")
    rsvp_status: RSVPStatus = Field(..., description="RSVP status")
    rsvp_date: Optional[datetime] = Field(None, description="Date when RSVP was received")
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
                "rsvp_status": "confirmed",
                "rsvp_date": "2024-02-15T10:30:00Z",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-02-15T10:30:00Z"
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
                        "created_at": "2024-01-15T10:30:00Z"
                    }
                ],
                "total": 150,
                "page": 1,
                "page_size": 20
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
                "maybe": 5
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
                        "email": "alice@example.com"
                    },
                    {
                        "name": "Bob Smith",
                        "phone_number": "+1234567891",
                        "email": "bob@example.com"
                    }
                ]
            }
        }

# Made with Bob