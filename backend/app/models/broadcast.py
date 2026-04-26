"""
Broadcast Model
Stores broadcast messages sent by planners to guests
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Enum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class BroadcastStatus(str, enum.Enum):
    """Broadcast status enumeration"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"


class Broadcast(Base):
    """
    Broadcast model - stores broadcast messages
    CRITICAL: Always includes planner_id AND event_id
    """
    __tablename__ = "broadcasts"
    
    # Primary Key
    broadcast_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation - MANDATORY
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    
    # Message Content
    message = Column(Text, nullable=False)
    
    # Targeting
    target_filter = Column(JSON, nullable=True)  # Filter criteria for recipients
    # Example: {"vip_level": "vip", "hotel_name": "Taj Palace"}
    
    # Recipients
    total_recipients = Column(Integer, default=0, nullable=False)
    sent_count = Column(Integer, default=0, nullable=False)
    delivered_count = Column(Integer, default=0, nullable=False)
    failed_count = Column(Integer, default=0, nullable=False)
    
    # Status
    status = Column(Enum(BroadcastStatus), default=BroadcastStatus.DRAFT, nullable=False)
    
    # Scheduling
    scheduled_at = Column(DateTime, nullable=True)
    
    # Personalization
    use_personalization = Column(Boolean, default=True, nullable=False)
    
    # Media
    media_url = Column(String(500), nullable=True)
    media_type = Column(String(50), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Error Tracking
    error_message = Column(Text, nullable=True)
    
    # Relationships
    event = relationship("Event", back_populates="broadcasts")
    
    def __repr__(self):
        return f"<Broadcast {self.broadcast_id}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "broadcast_id": str(self.broadcast_id),
            "event_id": str(self.event_id),
            "message": self.message,
            "total_recipients": self.total_recipients,
            "sent_count": self.sent_count,
            "delivered_count": self.delivered_count,
            "failed_count": self.failed_count,
            "status": self.status.value if self.status is not None else None,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at is not None else None,
        }

# Made with Bob
