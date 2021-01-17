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
from fastapi.responses import HTMLResponse, FileResponse

# routing
from .routers import images, users
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)
# APP declare
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# ROUTERS
app.include_router(images.router)
app.include_router(users.router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/NAS/{f1}/{f2}/{f3}/{file}", tags=["development", "serveImages"])
async def test(f1: str, f2: str, f3: str, file: str):
    """
    a hack to serve files from disk in development
    """
    return FileResponse(f"NAS/{f1}/{f2}/{f3}/{file}")
