import uvicorn

from typing import List
from fastapi import FastAPI

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from accounts import models, crud, schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_user_is_at_db(db, user_id):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = check_user_is_at_db(db=db, user_id=user_id)

    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = check_user_is_at_db(db=db, user_id=user_id)

    return crud.update_user_info(db=db, user=user)

@app.put("/users/changepw/{user_id}", response_model=schemas.User)
def update_user_password(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = check_user_is_at_db(db=db, user_id=user_id)

    return crud.update_user_password(db=db, user=user)
