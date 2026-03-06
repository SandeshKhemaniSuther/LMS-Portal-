from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.auth import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=hashed_password,
            role=user_data.role,
            phone_number=user_data.phone_number,
            bio=user_data.bio
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True
    
    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def search_users(self, query: str, skip: int = 0, limit: int = 100):
        return self.db.query(User).filter(
            User.first_name.ilike(f"%{query}%") |
            User.last_name.ilike(f"%{query}%") |
            User.email.ilike(f"%{query}%")
        ).offset(skip).limit(limit).all()
