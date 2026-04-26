"""
Planner Model
Represents event planners who manage events
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Planner(Base):
    """
    Planner model - represents event planners
    Each planner is a separate tenant with complete data isolation
    """
    __tablename__ = "planners"
    
    # Primary Key
    planner_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile Information
    full_name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    
    # WhatsApp Configuration
    whatsapp_number = Column(String(20), nullable=True)  # Planner's WhatsApp for notifications
    
    # Account Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    
    # Subscription/Tier
    subscription_tier = Column(String(50), default="free", nullable=False)  # free, pro, enterprise
    subscription_expires_at = Column(DateTime, nullable=True)
    
    # Limits based on tier
    max_events = Column(Integer, default=1, nullable=False)
    max_guests_per_event = Column(Integer, default=200, nullable=False)
    max_broadcasts_per_month = Column(Integer, default=50, nullable=False)
    
    # Preferences
    language_preference = Column(String(10), default="en", nullable=False)  # en, hi, kn
    timezone = Column(String(50), default="Asia/Kolkata", nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # Additional Info
    notes = Column(Text, nullable=True)
    
    # Relationships
    events = relationship("Event", back_populates="planner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Planner {self.email}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "planner_id": str(self.planner_id),
            "email": self.email,
            "phone": self.phone,
            "full_name": self.full_name,
            "company_name": self.company_name,
            "profile_image_url": self.profile_image_url,
            "whatsapp_number": self.whatsapp_number,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "subscription_tier": self.subscription_tier,
            "language_preference": self.language_preference,
            "timezone": self.timezone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }

# Made with Bob
