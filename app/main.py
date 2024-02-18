from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import auth, crud, models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=models.engine)

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except auth.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    return user

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = crud.create_user(db, user)
    access_token = auth.create_access_token({"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not auth.verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

@app.post("/notes", response_model=schemas.Note)
def create_note(
    note: schemas.NoteCreate,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_note = crud.create_note(db, note, current_user.id)
    return new_note

@app.get("/notes/{note_id}", response_model=schemas.Note)
def get_note(note_id: int, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = crud.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return note

@app.get("/notes", response_model=schemas.Note)
def get_notes(
    title: str = None,
    created_at: datetime = None,
    db: Session = Depends(get_db),
):
    if title or created_at:
        notes = crud.get_filtered_notes(db, title=title, created_at=created_at)
    else:
        notes = crud.get_notes(db)
    return notes

@app.get("/notes/{user_id}", response_model=schemas.Note)
def get_user_notes(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    notes = crud.get_user_notes(db, user_id)
    return notes