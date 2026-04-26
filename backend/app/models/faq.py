"""
FAQ Model
Stores frequently asked questions and answers for events
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class FAQ(Base):
    """
    FAQ model - stores event-specific FAQs for AI bot
    CRITICAL: Always includes planner_id AND event_id
    """
    __tablename__ = "faqs"
    
    # Primary Key
    faq_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation - MANDATORY
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    
    # FAQ Content
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # Categorization
    category = Column(String(100), nullable=True)  # venue, food, schedule, accommodation, etc.
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    
    # Vector Embedding (for semantic search)
    embedding = Column(String, nullable=True)  # Store as JSON string or use pgvector
    
    # Usage Statistics
    times_asked = Column(Integer, default=0, nullable=False)
    last_asked_at = Column(DateTime, nullable=True)
    
    # Relevance Score (for ranking)
    relevance_score = Column(Float, default=1.0, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="faqs")
    
    def __repr__(self):
        return f"<FAQ {self.question[:50]}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "faq_id": str(self.faq_id),
            "event_id": str(self.event_id),
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "tags": self.tags,
            "times_asked": self.times_asked,
            "relevance_score": self.relevance_score,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }

# Made with Bob
