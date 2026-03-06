from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, courses, enrollments, lessons, assignments, quizzes, forums, messages, reviews

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(forums.router, prefix="/forums", tags=["forums"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
