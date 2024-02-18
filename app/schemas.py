from datetime import datetime

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str
    email: str


class NoteUpdate(BaseModel):
    title: str
    content: str