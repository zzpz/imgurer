from typing import List, Optional, Dict
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

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str




class ImageBase(BaseModel):
    pass
    #hash
    #url
    #id
    #

class ImageCreate(ImageBase):
    url: str
    filename: str 
    thumb_url: Optional[str] = None
    dhash64: Optional[str] = None
    dhash128: Optional[str] = None
    phash: Optional[str] = None
    parsed: bool = False    
    in_bktree: bool = False
    

class ImageOut(ImageBase):
    url:str
    id: int
    #??

class MultiImageOut(ImageBase):
    images: List[Dict] # ID:url, ID:url

class ImageInDB(ImageBase):
    id: int
    url: str
    filename: str
    dhash64: Optional[str] = None
    dhash128: Optional[str] = None
    phash: Optional[str] = None
    parsed: Optional[bool] = False    
    in_bktree: Optional[bool] = False
    #??

class ImageBKTPopulate(ImageBase):
    id : int
    dhash128: str