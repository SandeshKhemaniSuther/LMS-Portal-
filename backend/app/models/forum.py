from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Forum(Base):
    __tablename__ = "forums"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    course = relationship("Course", back_populates="forums")
    posts = relationship("ForumPost", back_populates="forum", cascade="all, delete-orphan")

class ForumPost(Base):
    __tablename__ = "forum_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    forum_id = Column(Integer, ForeignKey("forums.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    reply_count = Column(Integer, default=0, nullable=False)
    last_reply_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    forum = relationship("Forum", back_populates="posts")
    author = relationship("User", back_populates="forum_posts")
    replies = relationship("ForumReply", back_populates="post", cascade="all, delete-orphan")

class ForumReply(Base):
    __tablename__ = "forum_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_reply_id = Column(Integer, ForeignKey("forum_replies.id"), nullable=True)
    is_solution = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    post = relationship("ForumPost", back_populates="replies")
    author = relationship("User")
    parent_reply = relationship("ForumReply", remote_side=[id])
    child_replies = relationship("ForumReply", back_populates="parent_reply")
