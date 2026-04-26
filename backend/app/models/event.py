"""
Event Model
Represents events managed by planners
"""
from sqlalchemy import Column, String, DateTime, Text, Enum, ForeignKey, Integer, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class EventStatus(str, enum.Enum):
    """Event status enumeration"""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class Event(Base):
    """
    Event model - represents individual events
    CRITICAL: Always includes planner_id for tenant isolation
    """
    __tablename__ = "events"
    
    # Primary Key
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation - MANDATORY
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    
    # Event Details
    event_name = Column(String(255), nullable=False)
    event_type = Column(String(100), nullable=False)  # wedding, corporate, birthday, etc.
    description = Column(Text, nullable=True)
    
    # Dates
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Location
    venue_name = Column(String(255), nullable=True)
    venue_address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India", nullable=False)
    
    # Status
    status = Column(Enum(EventStatus), default=EventStatus.DRAFT, nullable=False)
    
    # Guest Statistics
    total_guests = Column(Integer, default=0, nullable=False)
    guests_checked_in = Column(Integer, default=0, nullable=False)
    
    # Settings
    language = Column(String(10), default="en", nullable=False)  # en, hi, kn
    timezone = Column(String(50), default="Asia/Kolkata", nullable=False)
    
    # WhatsApp Bot Configuration
    bot_enabled = Column(Boolean, default=True, nullable=False)
    bot_greeting_message = Column(Text, nullable=True)
    bot_confidence_threshold = Column(Float, default=0.7, nullable=False)
    
    # Data Retention
    data_retention_days = Column(Integer, default=30, nullable=False)
    auto_delete_after_days = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    archived_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    planner = relationship("Planner", back_populates="events")
    guests = relationship("Guest", back_populates="event", cascade="all, delete-orphan")
    faqs = relationship("FAQ", back_populates="event", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="event", cascade="all, delete-orphan")
    broadcasts = relationship("Broadcast", back_populates="event", cascade="all, delete-orphan")
    support_requests = relationship("SupportRequest", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event {self.event_name}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "event_id": str(self.event_id),
            "planner_id": str(self.planner_id),
            "event_name": self.event_name,
            "event_type": self.event_type,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date is not None else None,
            "end_date": self.end_date.isoformat() if self.end_date is not None else None,
            "venue_name": self.venue_name,
            "venue_address": self.venue_address,
            "city": self.city,
            "status": self.status.value if self.status is not None else None,
            "total_guests": self.total_guests,
            "guests_checked_in": self.guests_checked_in,
            "language": self.language,
            "bot_enabled": self.bot_enabled,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None,
        }

# Made with Bob
