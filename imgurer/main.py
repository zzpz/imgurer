from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal,engine
from pydantic import BaseModel

# utility
from datetime import datetime, timedelta
from typing import Optional, List

from . import crud, schemas, models

# Front end
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# tokens
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# files (images + form data)
from fastapi import File, UploadFile, Form
import shutil

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_user_db():
    """
        
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# to get a string like this run:
# openssl rand -hex 32
#TODO:replace with environment variables
SECRET_KEY = "1a6fb4e63cca869677e4ca79e254ab1d56490894c8844d7838a40daf9cbe2988" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")





def authenticate_user(users_db: Session, username: str, password:str):
    """
        Takes username and password, retrieves user from DB, calls password verification on hashed password
    """
    user = crud.get_user(users_db, username)
    if not user:
        return False
    if not crud.verify_password(plain_password = password, hashed_password = user.hashed_password):
        return False
    return user


#### TOKEN
def create_access_token(
    data: dict
    , expires_delta: Optional[timedelta] = None
    ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    users_db:Session = Depends(get_user_db),
    token: str = Depends(oauth2_scheme)
    ):
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
        username : str = payload.get("")
    except JWTError:
        raise credentials_exception
    user = crud.get_user(users_db, username = token_data.username)
    if user is None:
        return credentials_exception
    return user

# async def get_current_user_values(current_user: = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    users_db: Session = Depends(get_user_db),
    form_data: OAuth2PasswordRequestForm = Depends()
    ):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}







@app.post("/user/new/",response_model= schemas.UserOut, status_code=201)
def create_user(
    user:schemas.UserCreate,
    user_db: Session = Depends(get_user_db)):
    """

    create a user (uname, pass, optional email) --> userCreate Schema

    """
    created_user = crud.create_user(users_db=user_db, user = user)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return created_user

@app.get("/user/all", response_model=schemas.UserOut)
def get_all(current_user = Depends(get_current_user)):
    return current_user   

@app.post("/image")
async def upload_image(image: UploadFile = File(...)):
    destination_folder = "./NAS/"
    with open(f"{destination_folder}desination.png","wb") as buffer:
        shutil.copyfileobj(image.file,buffer)

    return {"filename": image.filename, "content_type":image.content_type, "file":image.file}

@app.post("/images")
async def upload_images(images: List[UploadFile] = File(...)):
    destination_folder = "./NAS/"
    for image in images:
        with open(f"{destination_folder}{image.filename}","wb") as buffer:
            shutil.copyfileobj(image.file,buffer)




@app.get("/")
async def easy_upload(request: Request):


    return templates.TemplateResponse("upload.html",{
        "request": request
    })
