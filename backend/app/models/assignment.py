from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class SubmissionStatus(enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"
    REJECTED = "rejected"

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=True)
    max_score = Column(Float, default=100.0, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    allow_late_submission = Column(Boolean, default=False, nullable=False)
    late_penalty_percent = Column(Float, default=0.0, nullable=False)
    max_attempts = Column(Integer, default=1, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    instructor = relationship("User", back_populates="assignments_created")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    content = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=True)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.PENDING, nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    graded_at = Column(DateTime(timezone=True), nullable=True)
    attempt_number = Column(Integer, default=1, nullable=False)
    is_late = Column(Boolean, default=False, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("User", foreign_keys=[student_id], back_populates="submissions")
    enrollment = relationship("Enrollment", back_populates="submissions")
    grader = relationship("User", foreign_keys=[graded_by])
