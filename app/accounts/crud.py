# TODO: complete update method
from sqlalchemy.orm import Session

from . import models, schemas
from dotenv import load_dotenv

import hashlib
import os


load_dotenv()


def hashing_password(unhashed_password):
    h = hashlib.sha256()
    unhashed_password = unhashed_password + os.getenv('SALT')
    encoded_password = unhashed_password.encode()
    h.update(encoded_password)
    hashed_password = h.hexdigest()

    return hashed_password

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    hashed_password = hashing_password(unhashed_password=user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user_info(db: Session, user: schemas.UserUpdate):
    # userupdate 객체 email, password, is_active
    selected_user = db.query(models.User).filter(models.User.email == user.email).first()

    selected_user.is_active = user.is_active

    db.commit()
    db.refresh(selected_user)

    return selected_user

def update_user_password(db: Session, user: schemas.UserCreate):
    selected_user = db.query(models.User).filter(models.User.email == user.email).first()

    unhashed_password = user.password
    new_hashed_password = hashing_password(unhashed_password=unhashed_password)

    selected_user.hashed_password = new_hashed_password

    db.commit()
    db.refresh(selected_user)

    return selected_user



