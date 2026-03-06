from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User, UserRole
from app.models.course import Course, CourseStatus
from app.schemas.course import Course, CourseCreate, CourseUpdate, CourseDetail, CourseList
from app.services.course_service import CourseService

router = APIRouter()

@router.get("/", response_model=CourseList)
async def get_courses(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    level: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    instructor_id: Optional[int] = Query(None),
    status: Optional[CourseStatus] = Query(CourseStatus.PUBLISHED),
    db: Session = Depends(get_db)
):
    """Get courses list with pagination and filters"""
    course_service = CourseService(db)
    
    skip = (page - 1) * per_page
    courses, total = course_service.get_courses(
        skip=skip,
        limit=per_page,
        category_id=category_id,
        level=level,
        search=search,
        instructor_id=instructor_id,
        status=status
    )
    
    return CourseList(
        courses=courses,
        total=total,
        page=page,
        per_page=per_page
    )

@router.get("/featured", response_model=List[Course])
async def get_featured_courses(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured courses"""
    course_service = CourseService(db)
    return course_service.get_featured_courses(limit)

@router.get("/my-courses", response_model=List[Course])
async def get_my_courses(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get courses created by current user (instructor)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Instructor access required"
        )
    
    course_service = CourseService(db)
    return course_service.get_instructor_courses(current_user.id)

@router.get("/{course_id}", response_model=CourseDetail)
async def get_course(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get course details by ID"""
    course_service = CourseService(db)
    course = course_service.get_course_with_details(course_id, current_user.id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course

@router.post("/", response_model=Course)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new course (Instructor/Admin only)"""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Instructor access required"
        )
    
    course_service = CourseService(db)
    return course_service.create_course(course_data, current_user.id)

@router.put("/{course_id}", response_model=Course)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update course (Instructor/Admin only)"""
    course_service = CourseService(db)
    course = course_service.get_course_by_id(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is course instructor or admin
    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_course = course_service.update_course(course_id, course_data)
    return updated_course

@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete course (Instructor/Admin only)"""
    course_service = CourseService(db)
    course = course_service.get_course_by_id(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if user is course instructor or admin
    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    success = course_service.delete_course(course_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete course with enrollments"
        )
    
    return {"message": "Course deleted successfully"}

@router.post("/{course_id}/thumbnail")
async def upload_course_thumbnail(
    course_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload course thumbnail"""
    course_service = CourseService(db)
    course = course_service.get_course_by_id(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check permissions
    if course.instructor_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    thumbnail_url = await course_service.upload_thumbnail(course_id, file)
    return {"thumbnail_url": thumbnail_url}
