from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dependencies.auth import  verify_password
from config import create_access_token
from schemas.users import Token, TokenData
from models.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:    
    
    @staticmethod
    def authenticate_user(db:Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    @staticmethod
    def login_user(user: User)-> Token:
        data = {"sub": user.email, "id": user.id}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data=data, expires_delta=access_token_expires)
        return Token(access_token=access_token)
    

user_auth_service = AuthService()