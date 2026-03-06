from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from app.models.course import CourseStatus, CourseLevel, Category

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    icon_url: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    icon_url: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    category_id: Optional[int] = None
    level: CourseLevel = CourseLevel.BEGINNER
    price: float = 0.0
    currency: str = "USD"
    language: str = "en"
    duration_hours: Optional[int] = None
    max_students: Optional[int] = None
    certificate_available: bool = False

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    category_id: Optional[int] = None
    level: Optional[CourseLevel] = None
    status: Optional[CourseStatus] = None
    thumbnail_url: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    duration_hours: Optional[int] = None
    max_students: Optional[int] = None
    certificate_available: Optional[bool] = None
    is_featured: Optional[bool] = None

class Course(CourseBase):
    id: int
    instructor_id: int
    status: CourseStatus
    thumbnail_url: Optional[str] = None
    is_featured: bool
    rating: float
    rating_count: int
    enrollment_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CourseDetail(Course):
    instructor: dict
    category: Optional[Category] = None
    lessons: List[dict] = []
    enrollments_count: int

class CourseList(BaseModel):
    courses: List[Course]
    total: int
    page: int
    per_page: int
