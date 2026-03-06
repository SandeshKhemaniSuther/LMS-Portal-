from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class MessageType(enum.Enum):
    TEXT = "text"
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class MessageStatus(enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.TEXT, nullable=False)
    file_url = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT, nullable=False)
    is_deleted_by_sender = Column(Boolean, default=False, nullable=False)
    is_deleted_by_receiver = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="messages_sent")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="messages_received")
