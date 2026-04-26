"""
Guest Model
Represents guests attending events
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class RelationType(str, enum.Enum):
    """Guest relation type enumeration"""
    UNCLE = "uncle"
    AUNT = "aunt"
    FRIEND = "friend"
    COUSIN = "cousin"
    COLLEAGUE = "colleague"
    FAMILY = "family"
    VIP = "vip"
    OTHER = "other"


class TonePreference(str, enum.Enum):
    """Message tone preference"""
    FORMAL = "formal"
    CASUAL = "casual"
    RESPECTFUL = "respectful"
    FRIENDLY = "friendly"


class Guest(Base):
    """
    Guest model - represents event attendees
    CRITICAL: Always includes planner_id AND event_id for complete isolation
    """
    __tablename__ = "guests"
    
    # Primary Key
    guest_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation - MANDATORY (both planner_id and event_id)
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, index=True)  # WhatsApp number
    email = Column(String(255), nullable=True)
    
    # Personalization Data
    relation_type = Column(String(50), default=RelationType.OTHER.value, nullable=False)
    tone_preference = Column(String(50), default=TonePreference.FRIENDLY.value, nullable=False)
    language = Column(String(10), default="en", nullable=False)  # en, hi, kn
    
    # VIP Status
    vip_level = Column(String(20), default="regular", nullable=False)  # regular, vip, close, casual
    
    # Health & Dietary
    health_notes = Column(JSON, nullable=True)  # ["diabetes", "allergy_nuts"]
    food_preference = Column(String(50), nullable=True)  # veg, non-veg, vegan, jain
    dietary_restrictions = Column(Text, nullable=True)
    
    # Accommodation
    hotel_name = Column(String(255), nullable=True)
    room_number = Column(String(50), nullable=True)
    check_in_date = Column(DateTime, nullable=True)
    check_out_date = Column(DateTime, nullable=True)
    
    # Attendance
    is_attending = Column(Boolean, default=True, nullable=False)
    checked_in = Column(Boolean, default=False, nullable=False)
    checked_in_at = Column(DateTime, nullable=True)
    
    # Plus Ones
    plus_ones = Column(Integer, default=0, nullable=False)
    
    # Contact Preferences
    whatsapp_opted_in = Column(Boolean, default=True, nullable=False)
    notifications_enabled = Column(Boolean, default=True, nullable=False)
    
    # Additional Info
    notes = Column(Text, nullable=True)
    custom_fields = Column(JSON, nullable=True)  # Flexible additional data
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_message_at = Column(DateTime, nullable=True)
    
    # Privacy (for data retention)
    data_deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    event = relationship("Event", back_populates="guests")
    conversations = relationship("Conversation", back_populates="guest", cascade="all, delete-orphan")
    support_requests = relationship("SupportRequest", back_populates="guest", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Guest {self.name} - {self.phone}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "guest_id": str(self.guest_id),
            "planner_id": str(self.planner_id),
            "event_id": str(self.event_id),
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "relation_type": self.relation_type,
            "tone_preference": self.tone_preference,
            "language": self.language,
            "vip_level": self.vip_level,
            "food_preference": self.food_preference,
            "hotel_name": self.hotel_name,
            "room_number": self.room_number,
            "is_attending": self.is_attending,
            "checked_in": self.checked_in,
            "whatsapp_opted_in": self.whatsapp_opted_in,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at is not None else None,
        }

# Made with Bob
