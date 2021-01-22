from fastapi import FastAPI, Request, Depends, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import engine
from pydantic import BaseModel

# utility
from datetime import datetime, timedelta
from typing import Optional


# Front end
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

# routing
from .routers import images, users
from fastapi.staticfiles import StaticFiles

# config
from .dependencies import get_settings
from . import config

# APP declare
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# ROUTERS
app.include_router(images.router)
app.include_router(users.router)

templates = Jinja2Templates(directory="templates")

# STARTUP
@app.on_event("startup")
async def startup_event():
    """
    Things that need to occur on startup:
    - rebuildBKTree()
    - database??
    - filestore??
    """

    bktree = None
    pass


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/t", tags=["experimenting"])
async def fp_upload(request: Request):
    return templates.TemplateResponse("fp_upload.html", {"request": request})


@app.get("/NAS/{f1}/{f2}/{f3}/{file}", tags=["development", "serveImages"])
async def file_server(f1: str, f2: str, f3: str, file: str):
    """
    a hack to serve files from disk
    """
    return FileResponse(f"NAS/{f1}/{f2}/{f3}/{file}")


@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    """
    Returns information about the application taken from settings
    """
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
    }


# TODO: testing with test settings
# from fastapi.testclient import TestClient

# from . import config, main

# client = TestClient(main.app)


# def get_settings_override():
#     return config.Settings(admin_email="testing_admin@example.com")


# main.app.dependency_overrides[main.get_settings] = get_settings_override


# def test_app():

#     response = client.get("/info")
#     data = response.json()
#     assert data == {
#         "app_name": "Awesome API",
#         "admin_email": "testing_admin@example.com",
#         "items_per_user": 50,
#     }