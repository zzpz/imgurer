# routing
from fastapi import Depends, FastAPI, HTTPException, status

# utility
from datetime import datetime, timedelta
import random
from typing import Optional, List

# SQL
from sqlalchemy.orm import Session
from . import models, schemas  # TokenData
from .database import SessionLocal, engine  # singular database for users and images
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.strategy_options import load_only
from sqlalchemy import func

# images
from fastapi import UploadFile

# password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# to get a string like this run:
# openssl rand -hex 32
# TODO:replace with environment variables
SECRET_KEY = "1a6fb4e63cca869677e4ca79e254ab1d56490894c8844d7838a40daf9cbe2988"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#### PASSWORDS
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# CRUD
# Create, Read, Update, and Delete


def create_user(users_db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username, hashed_password=get_password_hash(user.password)
    )
    try:
        users_db.add(db_user)
        users_db.commit()
        users_db.refresh(db_user)
        return user
    except IntegrityError as duplicate_uname:
        return None


def get_user(users_db: Session, username: str):
    try:
        user = (
            users_db.query(models.User).filter(models.User.username == username).first()
        )
        return schemas.UserInDB(
            username=user.username, hashed_password=user.hashed_password
        )
    except NoResultFound as not_found:
        return None


def create_image(images_db: Session, image: schemas.ImageCreate):
    """
    connect to provided database Session, create image in db
    """
    db_image = models.Image(
        parsed=False,
        dhash64=None,
        phash=None,
        dhash128=image.dhash128,
        url=image.url,
        url_thumb=image.thumb_url,
        filename=image.filename,
    )
    images_db.add(db_image)
    images_db.commit()
    images_db.refresh(db_image)
    return db_image


def get_image(images_db: Session, id: int) -> schemas.ImageInDB:
    try:
        img = images_db.query(models.Image).filter(models.Image.id == id).first()
        if not img:  # not catching an exception here
            return None
        image_inDB = schemas.ImageInDB(
            id=img.id, url=img.url, filename=img.filename, dhash128=img.dhash128
        )
        return image_inDB
    except NoResultFound as not_found:  # doesn't catch empty db?
        return None


def get_bkt_reload_images(images_db: Session):
    """
    this seems like a hazardous query
    """
    all_images = images_db.query(models.Image).all()
    bkt_id_dhash128 = []
    for image in all_images:
        bkt_id_dhash128.append(
            schemas.ImageBKTPopulate(id=image.id, dhash128=image.dhash128)
        )

    return bkt_id_dhash128


def browse_images(images_db: Session) -> schemas.MultiImageOut:
    """
    Here, have up to N random images from the database
    """
    n: int = 48
    number = images_db.query(func.count(models.Image.id)).scalar()
    randoms = random.sample(range(1, number + 1), min(n, number))

    images_in_db = (
        images_db.query(models.Image).filter(models.Image.id.in_(randoms)).all()
    )

    if not images_in_db:  # not catching an exception here
        return None
    images_out = []
    for image in images_in_db:
        d = {"id": image.id, "url": image.url, "thumb_url": image.url_thumb}
        images_out.append(d)

    images = schemas.MultiImageOut(images=images_out)
    return images


def get_images(images_db: Session, ids: [int]) -> schemas.MultiImageOut:
    """
    should be optional ints provided
    """
    try:
        images_in_db = (
            images_db.query(models.Image).filter(models.Image.id.in_(ids)).all()
        )
        if not images_in_db:  # not catching an exception here
            return None
        images_out = []
        for image in images_in_db:
            d = {"id": image.id, "url": image.url, "thumb_url": image.url_thumb}
            images_out.append(d)

        images = schemas.MultiImageOut(images=images_out)
        return images
    except NoResultFound as not_found:
        return None


def create_tags(images_db: Session):
    ...
    # stub


def update_user():
    pass


def delete_user():
    pass