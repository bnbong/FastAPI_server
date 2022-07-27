# TODO: complete update method
from sqlalchemy.orm import Session

from . import models, schemas
from dotenv import load_dotenv

import hashlib
import os


load_dotenv()


def hashing_password(user: schemas.UserCreate):
    h = hashlib.sha256()
    unhashed_password = user.password + os.getenv('SALT')
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
    hashed_password = hashing_password(user=user)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user(db: Session, user: schemas.UserUpdate):
    # userupdate 객체 email, password, is_active
    selected_user = db.query(models.User).filter(models.User.email == user.email).first()

    user_dict = {k: v for k, v in selected_user.items()}

    for key, value in user_dict.items():
        if key == 'password' and value is not None:
            hashed_password = hashing_password(user=user)

            value = hashed_password

        setattr(selected_user, key, value)

    db.commit()

    return 

