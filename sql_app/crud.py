#routing
from fastapi import Depends, FastAPI, HTTPException, status

#utility
from datetime import datetime, timedelta
from typing import Optional

#SQL
from sqlalchemy.orm import Session
from . import models, schemas #TokenData
from .database import SessionLocal, engine #singular database for users and images

#password + tokens
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# to get a string like this run:
# openssl rand -hex 32
#TODO:replace with environment variables
SECRET_KEY = "1a6fb4e63cca869677e4ca79e254ab1d56490894c8844d7838a40daf9cbe2988" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)




#CRUD
#Create, Read, Update, and Delete


def create_user(users_db:Session,user:schemas.UserCreate):
    db_user = models.User(username=user.username,password = user.password)
    pass

def get_user(users_db: Session, username: str):
    
    pass

def update_user():
    pass

def delete_user():
    pass

#tokens authentication
def authenticate_user(users_db: Session, username: str, password:str):
    """
        Takes username and password, retrieves user from DB, calls password verification on hashed password
    """
    # multiple tries / security prevention here ()
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(plain_password = password, hashed_password = user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(users_db:Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username = username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username = token_data.username)
    if user is None:
        return credentials_exception
    return user

async def get_current_user_values(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
