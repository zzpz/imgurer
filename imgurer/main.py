from fastapi import FastAPI, Request, Depends, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine
from pydantic import BaseModel

# utility
from datetime import datetime, timedelta
from typing import Optional

from . import crud, schemas, models

# Front end
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
# routing
from .routers import images, users

models.Base.metadata.create_all(bind=engine)

# APP declare 
app = FastAPI()
# ROUTERS 
app.include_router(
    images.router
    )
app.include_router(
    users.router
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html",{
        "request": request
    })
