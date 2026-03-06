from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class QuestionType(enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    FILL_BLANK = "fill_blank"

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    time_limit_minutes = Column(Integer, nullable=True)
    max_attempts = Column(Integer, default=3, nullable=False)
    passing_score = Column(Float, default=70.0, nullable=False)
    shuffle_questions = Column(Boolean, default=False, nullable=False)
    show_correct_answers = Column(Boolean, default=False, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lesson = relationship("Lesson", back_populates="quiz")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    points = Column(Float, default=1.0, nullable=False)
    explanation = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question", cascade="all, delete-orphan")

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    
    # Relationships
    question = relationship("QuizQuestion", back_populates="answers")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    attempt_number = Column(Integer, default=1, nullable=False)
    
    # Relationships
    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("User")
    enrollment = relationship("Enrollment")
    responses = relationship("QuizResponse", back_populates="attempt", cascade="all, delete-orphan")

class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    answer_id = Column(Integer, ForeignKey("quiz_answers.id"), nullable=True)
    text_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    points_earned = Column(Float, nullable=True)
    
    # Relationships
    attempt = relationship("QuizAttempt", back_populates="responses")
    question = relationship("QuizQuestion")
    answer = relationship("QuizAnswer")
