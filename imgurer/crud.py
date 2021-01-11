#routing
from fastapi import Depends, FastAPI, HTTPException, status

#utility
from datetime import datetime, timedelta
from typing import Optional

#SQL
from sqlalchemy.orm import Session
from . import models, schemas #TokenData
from .database import SessionLocal, engine #singular database for users and images
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound



#password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#### PASSWORDS
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)



#CRUD
#Create, Read, Update, and Delete


def create_user(users_db:Session,user:schemas.UserCreate):
    db_user = models.User(username=user.username,hashed_password = get_password_hash(user.password))
    try:
        users_db.add(db_user)
        users_db.commit()
        users_db.refresh(db_user)
        return user
    except IntegrityError as duplicate_uname:
        return None
        


def get_user(users_db: Session, username: str):
    try:
        user = users_db.query(models.User).filter(models.User.username==username).first()
        return schemas.UserInDB(username = user.username, hashed_password =user.hashed_password)
    except NoResultFound as not_found:
        return None


    

def update_user():
    pass

def delete_user():
    pass