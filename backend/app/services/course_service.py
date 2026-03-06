from sqlalchemy.orm import Session
from typing import List, Tuple, Optional
from fastapi import UploadFile
import os
import uuid
from app.models.course import Course, Category, CourseStatus, CourseLevel
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate
from app.core.config import settings

class CourseService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_course_by_id(self, course_id: int) -> Optional[Course]:
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def get_courses(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        level: Optional[str] = None,
        search: Optional[str] = None,
        instructor_id: Optional[int] = None,
        status: CourseStatus = CourseStatus.PUBLISHED
    ) -> Tuple[List[Course], int]:
        query = self.db.query(Course).filter(Course.status == status)
        
        if category_id:
            query = query.filter(Course.category_id == category_id)
        
        if level:
            query = query.filter(Course.level == level)
        
        if instructor_id:
            query = query.filter(Course.instructor_id == instructor_id)
        
        if search:
            query = query.filter(
                Course.title.ilike(f"%{search}%") |
                Course.description.ilike(f"%{search}%")
            )
        
        total = query.count()
        courses = query.offset(skip).limit(limit).all()
        
        return courses, total
    
    def get_featured_courses(self, limit: int = 10) -> List[Course]:
        return self.db.query(Course).filter(
            Course.is_featured == True,
            Course.status == CourseStatus.PUBLISHED
        ).limit(limit).all()
    
    def get_instructor_courses(self, instructor_id: int) -> List[Course]:
        return self.db.query(Course).filter(
            Course.instructor_id == instructor_id
        ).all()
    
    def get_course_with_details(self, course_id: int, user_id: Optional[int] = None) -> Optional[dict]:
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        
        # Get instructor info
        instructor = self.db.query(User).filter(User.id == course.instructor_id).first()
        
        # Get category info
        category = self.db.query(Category).filter(Category.id == course.category_id).first()
        
        # Get lessons count
        lessons_count = self.db.query(Course).filter(Course.id == course_id).count()
        
        # Check if user is enrolled
        is_enrolled = False
        if user_id:
            from app.models.enrollment import Enrollment
            enrollment = self.db.query(Enrollment).filter(
                Enrollment.course_id == course_id,
                Enrollment.student_id == user_id
            ).first()
            is_enrolled = enrollment is not None
        
        return {
            **course.__dict__,
            "instructor": {
                "id": instructor.id,
                "first_name": instructor.first_name,
                "last_name": instructor.last_name,
                "avatar_url": instructor.avatar_url
            } if instructor else None,
            "category": category,
            "lessons_count": lessons_count,
            "is_enrolled": is_enrolled
        }
    
    def create_course(self, course_data: CourseCreate, instructor_id: int) -> Course:
        db_course = Course(
            title=course_data.title,
            description=course_data.description,
            short_description=course_data.short_description,
            instructor_id=instructor_id,
            category_id=course_data.category_id,
            level=course_data.level,
            price=course_data.price,
            currency=course_data.currency,
            language=course_data.language,
            duration_hours=course_data.duration_hours,
            max_students=course_data.max_students,
            certificate_available=course_data.certificate_available,
            status=CourseStatus.DRAFT
        )
        
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course
    
    def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        course = self.get_course_by_id(course_id)
        if not course:
            return None
        
        update_data = course_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def delete_course(self, course_id: int) -> bool:
        course = self.get_course_by_id(course_id)
        if not course:
            return False
        
        # Check if course has enrollments
        if course.enrollment_count > 0:
            return False
        
        self.db.delete(course)
        self.db.commit()
        return True
    
    async def upload_thumbnail(self, course_id: int, file: UploadFile) -> str:
        # Create unique filename
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(settings.UPLOAD_DIR, "course-thumbnails")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Update course thumbnail_url
        thumbnail_url = f"/uploads/course-thumbnails/{unique_filename}"
        course = self.get_course_by_id(course_id)
        course.thumbnail_url = thumbnail_url
        self.db.commit()
        
        return thumbnail_url
