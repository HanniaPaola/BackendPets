from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Juan Pérez")
    email: EmailStr = Field(..., example="juan@correo.com")
    password: str = Field(..., min_length=6, example="mipassword123")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="juan@correo.com")
    password: str = Field(..., example="mipassword123")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=6)
