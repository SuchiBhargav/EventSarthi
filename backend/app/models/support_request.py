"""
Support Request Model
Tracks guest requests that need planner attention
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class RequestCategory(str, enum.Enum):
    """Support request category"""
    TRANSPORT = "transport"
    HELP = "help"
    FOOD = "food"
    MEDICAL = "medical"
    ACCOMMODATION = "accommodation"
    VENUE_QUERY = "venue_query"
    UNKNOWN = "unknown"


class RequestStatus(str, enum.Enum):
    """Support request status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SupportRequest(Base):
    """
    Support Request model - tracks guest requests requiring planner intervention
    CRITICAL: Always includes planner_id AND event_id
    """
    __tablename__ = "support_requests"
    
    # Primary Key
    request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation - MANDATORY
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.guest_id"), nullable=False, index=True)
    
    # Request Details
    category = Column(Enum(RequestCategory), default=RequestCategory.UNKNOWN, nullable=False)
    message = Column(Text, nullable=False)
    
    # Status
    status = Column(Enum(RequestStatus), default=RequestStatus.OPEN, nullable=False, index=True)
    
    # Assignment
    assigned_to = Column(UUID(as_uuid=True), nullable=True)  # Can be assigned to specific planner/staff
    
    # Priority
    priority = Column(String(20), default="normal", nullable=False)  # low, normal, high, urgent
    
    # Response
    planner_response = Column(Text, nullable=True)
    response_sent_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    event = relationship("Event", back_populates="support_requests")
    guest = relationship("Guest", back_populates="support_requests")
    
    def __repr__(self):
        return f"<SupportRequest {self.request_id} - {self.category}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "request_id": str(self.request_id),
            "event_id": str(self.event_id),
            "guest_id": str(self.guest_id),
            "category": self.category.value if self.category else None,
            "message": self.message,
            "status": self.status.value if self.status else None,
            "priority": self.priority,
            "planner_response": self.planner_response,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }

# Made with Bob
