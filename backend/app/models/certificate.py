from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Certificate(Base):
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    certificate_url = Column(String(500), nullable=False)
    certificate_number = Column(String(100), unique=True, nullable=False, index=True)
    issued_date = Column(DateTime(timezone=True), server_default=func.now())
    template_id = Column(Integer, nullable=True)
    metadata = Column(Text, nullable=True)  # JSON data for certificate details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    enrollment = relationship("Enrollment")
