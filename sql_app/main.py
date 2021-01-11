from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal,engine
from pydantic import BaseModel


def get_user_db():
    """
        
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()