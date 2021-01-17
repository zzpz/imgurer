from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session


from ..dependencies import valid_content_length, get_nas, get_user_db
from ..schemas import Token, TokenData, UserOut, UserCreate

# password and security
from ..crud import get_user, verify_password, create_user
from ..crud import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# tokens
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# utility
from datetime import datetime, timedelta
from typing import Optional

# frontend
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends()]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=router.prefix + "/token")
templates = Jinja2Templates(directory="templates")


def authenticate_user(users_db: Session, username: str, password: str):
    """
    Takes username and password, retrieves user from DB, calls password verification on hashed password
    """
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(
        plain_password=password, hashed_password=user.hashed_password
    ):
        return False
    return user


#### TOKEN
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    users_db: Session = Depends(get_user_db), token: str = Depends(oauth2_scheme)
):
    """
    Returns current authorized user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        username: str = payload.get("")
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        return credentials_exception
    return user


# async def get_current_user_values(current_user: = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@router.post("/new", response_model=UserOut, status_code=201)
def new_user(user: UserCreate, user_db: Session = Depends(get_user_db)):
    """

    create a user (uname, pass, optional email)

    """
    created_user = create_user(users_db=user_db, user=user)
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return created_user


@router.get("/all", response_model=UserOut)
def get_all(current_user=Depends(get_current_user)):
    """
    if current user is authorized will return UserOut schema of all users in database
    """
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    users_db: Session = Depends(get_user_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Creates a JWT token given correct user login form data
    """
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