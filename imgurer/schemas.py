from typing import List, Optional
from pydantic import BaseModel
import datetime



# tokens, passwords, sessions
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    permissions: Optional[int] = None # TODO:implement permissioning
    #other token data? permissions? identifiers? 

# Users

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    email : Optional[str] = None

class UserInDB(UserBase):
    hashed_password: str

class UserOut(UserBase):
    email: Optional[str] = None
    pass


class ImageBase(BaseModel):
    ...
    #hash
    #url
    #id
    #


