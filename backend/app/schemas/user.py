from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.STUDENT
    phone_number: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    email_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    email: Optional[str] = None

class UserProfile(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: UserRole
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
