from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class EnrollmentStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"
    SUSPENDED = "suspended"

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE, nullable=False)
    progress_percentage = Column(Float, default=0.0, nullable=False)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    certificate_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    lesson_progress = relationship("LessonProgress", back_populates="enrollment", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="enrollment", cascade="all, delete-orphan")

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    watch_time_seconds = Column(Integer, default=0, nullable=False)
    last_position_seconds = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    enrollment = relationship("Enrollment", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress_records")
