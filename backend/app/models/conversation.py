"""
Conversation and Message Models
Tracks WhatsApp conversations between guests and the bot
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Integer, Enum, Float
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class MessageDirection(str, enum.Enum):
    """Message direction"""
    INBOUND = "inbound"   # From guest to bot
    OUTBOUND = "outbound"  # From bot to guest


class MessageStatus(str, enum.Enum):
    """WhatsApp message status"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Conversation(Base):
    """
    Conversation model - tracks conversation sessions with guests
    """
    __tablename__ = "conversations"
    
    # Primary Key
    conversation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.guest_id"), nullable=False, index=True)
    
    # WhatsApp Session
    whatsapp_phone = Column(String(20), nullable=False)
    session_active = Column(Boolean, default=True, nullable=False)
    
    # Conversation Context (for AI)
    context = Column(JSON, nullable=True)  # Store conversation context
    
    # Statistics
    message_count = Column(Integer, default=0, nullable=False)
    escalated = Column(Boolean, default=False, nullable=False)
    escalated_at = Column(DateTime, nullable=True)
    
    # Metadata
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_message_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    guest = relationship("Guest", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation {self.conversation_id}>"


class Message(Base):
    """
    Message model - individual messages in conversations
    """
    __tablename__ = "messages"
    
    # Primary Key
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Tenant Isolation
    planner_id = Column(UUID(as_uuid=True), ForeignKey("planners.planner_id"), nullable=False, index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.conversation_id"), nullable=False, index=True)
    
    # Message Content
    direction = Column(Enum(MessageDirection), nullable=False)
    content = Column(Text, nullable=False)
    
    # WhatsApp Metadata
    whatsapp_message_id = Column(String(255), nullable=True, unique=True, index=True)
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT, nullable=False)
    
    # AI Processing
    intent = Column(String(100), nullable=True)  # Detected intent
    confidence = Column(Float, nullable=True)  # AI confidence score
    ai_generated = Column(Boolean, default=False, nullable=False)
    
    # Response Metadata
    response_time_ms = Column(Integer, nullable=True)  # Time taken to generate response
    
    # Media
    media_url = Column(String(500), nullable=True)
    media_type = Column(String(50), nullable=True)  # image, document, audio, video
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message {self.message_id} - {self.direction}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "message_id": str(self.message_id),
            "conversation_id": str(self.conversation_id),
            "direction": self.direction.value if self.direction is not None else None,
            "content": self.content,
            "status": self.status.value if self.status is not None else None,
            "intent": self.intent,
            "confidence": self.confidence,
            "ai_generated": self.ai_generated,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
        }

# Made with Bob
