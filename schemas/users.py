from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
   

class UserCreate(UserBase):
    password: str
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = "Admin"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

class UserOut(UserBase):
    id: UUID
    role: str = "Admin"

    model_config = {
        "from_attributes": True
         }


class LoginResponse(BaseModel):
    user: UserOut
    token: Token
