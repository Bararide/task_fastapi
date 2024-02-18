from datetime import datetime
from sqlalchemy.orm import Session
from . import models as dh, schemas

from . import auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = dh.User(username=user.username, email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_username(db: Session, username: str) -> dh.User:
    return db.query(dh.User).filter(dh.User.username == username).first()

def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = dh.Note(
        title=note.title, content=note.content, user_id=user_id,
        created_at=datetime.now(), updated_at=datetime.now()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

def get_users(db: Session):
    return db.query(db.User).all()

def get_notes(db: Session):
    return db.query(db.Note).all()

def get_user(db: Session, user_id: int):
    return db.query(db.User).filter(db.User.id == user_id).first()

def get_note(db: Session, note_id: int):
    return db.query(db.Note).filter(db.Note.id == note_id).first()

def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        for attr, value in user.dict(exclude_unset=True).items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def update_note(db: Session, note: schemas.NoteUpdate, note_id: int):
    db_note = get_note(db, note_id)
    if db_note:
        for attr, value in note.dict(exclude_unset=True).items():
            setattr(db_note, attr, value)

        db_note.updated_at = datetime.now()
        db.commit()
        db.refresh(db_note)
    return db_note

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def delete_note(db: Session, note_id: int):
    db_note = get_note(db, note_id)
    if db_note:
        db.delete(db_note)
        db.commit()
    return db_note

def get_user_notes(db: Session, user_id: int):
    return db.query(dh.Note).filter(dh.Note.user_id == user_id).all()

def get_filtered_notes(db: Session, title: str = None, created_at: datetime = None):
    query = db.query(dh.Note)
    if title:
        query = query.filter(dh.Note.title.ilike(f"%{title}%"))
    if created_at:
        query = query.filter(dh.Note.created_at == created_at)
    return query.all()