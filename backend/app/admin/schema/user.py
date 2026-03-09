from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime 
from typing import Optional
from uuid import UUID

class AuthSchema(BaseModel):
    username: str
    password: str | None

class UserSchema(BaseModel):
    id: UUID
    role: str
    name: str
    uid: Optional[str] = None
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    archived: bool
    registered: bool

class UserCreateSchema(BaseModel):
    id: UUID
    role: str
    name: str
    uid: Optional[str] = None
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    email: Optional[str] = None
    archived: bool
    registered: Optional[bool]
    ms_created: datetime
    ms_updated: datetime
    updated_at: datetime
    created_at: datetime

class UserInDbSchema(UserCreateSchema):
    hash_password: Optional[str]

class UserRoleSchema(BaseModel):
    role: str