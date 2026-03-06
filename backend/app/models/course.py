from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class CourseStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class CourseLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    level = Column(Enum(CourseLevel), default=CourseLevel.BEGINNER, nullable=False)
    status = Column(Enum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    thumbnail_url = Column(String(500), nullable=True)
    price = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    duration_hours = Column(Integer, nullable=True)
    max_students = Column(Integer, nullable=True)
    certificate_available = Column(Boolean, default=False, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    rating = Column(Float, default=0.0, nullable=False)
    rating_count = Column(Integer, default=0, nullable=False)
    enrollment_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    instructor = relationship("User", back_populates="taught_courses")
    category = relationship("Category", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    forums = relationship("Forum", back_populates="course", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="course", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    icon_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    parent = relationship("Category", remote_side=[id])
    children = relationship("Category", back_populates="parent")
    courses = relationship("Course", back_populates="category")
