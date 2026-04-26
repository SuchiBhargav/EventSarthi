"""
Schedule Model
Stores event schedules and timings
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class Schedule(Base):
    """
    Schedule model - stores event schedule items
    CRITICAL: Always includes planner_id AND event_id
    """
    __tablename__ = "schedules"
    
    # Primary Key
    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation - MANDATORY
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    
    # Schedule Details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Timing
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=True)
    
    # Location
    venue = Column(String(255), nullable=True)
    location_details = Column(Text, nullable=True)
    
    # Categorization
    category = Column(String(100), nullable=True)  # ceremony, reception, sangeet, etc.
    
    # Notifications
    send_reminder = Column(Boolean, default=True, nullable=False)
    reminder_minutes_before = Column(Integer, default=30, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="schedules")
    
    def __repr__(self):
        return f"<Schedule {self.title}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "schedule_id": str(self.schedule_id),
            "event_id": str(self.event_id),
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "venue": self.venue,
            "category": self.category,
            "send_reminder": self.send_reminder,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

# Made with Bob
