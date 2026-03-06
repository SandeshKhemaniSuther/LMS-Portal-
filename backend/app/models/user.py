from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class UserRole(enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_number = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="student")
    taught_courses = relationship("Course", back_populates="instructor")
    assignments_created = relationship("Assignment", back_populates="instructor")
    submissions = relationship("Submission", back_populates="student")
    forum_posts = relationship("ForumPost", back_populates="author")
    messages_sent = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    messages_received = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def has_role(self, role: UserRole) -> bool:
        return self.role == role
