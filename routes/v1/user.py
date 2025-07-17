from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserUpdate, LoginResponse, UserLogin
from database.database import get_db
from crud.user import user_crud
from services.auth import user_auth_service

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = user_crud.create_user(db,user)
    return {"detail": "User created successfully", "user": new_user}

@router.get("/users/", status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    all_users =user_crud.get_users(db)
    return {"users": all_users}

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    user = user_auth_service.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = user_auth_service.login_user(user)
    return {
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email
        },
        "token": token 
    }