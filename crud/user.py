from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserUpdate 
from dependencies.auth import  get_password_hash
from models.user import User 



class UserCRUD:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
         # Check if username exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        # Check if email exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )
        hashed_password = get_password_hash(user_data.password)
        new_user = User( username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def get_users(db:Session):
        users = db.query(User).all()
        return users
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        return user
    
    
user_crud = UserCRUD()


    