from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class LessonType(enum.Enum):
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    LIVE_STREAM = "live_stream"

class LessonStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    lesson_type = Column(Enum(LessonType), default=LessonType.VIDEO, nullable=False)
    status = Column(Enum(LessonStatus), default=LessonStatus.DRAFT, nullable=False)
    content_url = Column(String(500), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    transcript = Column(Text, nullable=True)
    download_url = Column(String(500), nullable=True)
    is_free = Column(Boolean, default=False, nullable=False)
    is_required = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="lessons")
    progress_records = relationship("LessonProgress", back_populates="lesson")
    quiz = relationship("Quiz", back_populates="lesson", uselist=False, cascade="all, delete-orphan")
    resources = relationship("LessonResource", back_populates="lesson", cascade="all, delete-orphan")

class LessonResource(Base):
    __tablename__ = "lesson_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=True)
    is_downloadable = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lesson = relationship("Lesson", back_populates="resources")
