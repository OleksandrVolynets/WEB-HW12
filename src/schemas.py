from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    id: int
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str = Field(max_length=150)
    phone_number: str = Field(max_length=20)
    birthday: date
    description: str = Field(max_length=1500, default='')


class ContactResponse(ContactBase):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    description: str

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
