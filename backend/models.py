from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str


class MessageResponse(BaseModel):
    id: str
    name: str
    email: str
    message: str
    created_at: str

    class Config:
        from_attributes = True

