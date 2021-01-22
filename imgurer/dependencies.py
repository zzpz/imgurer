from fastapi import Header
from .database import SessionLocal

# config
from functools import lru_cache
from . import config


@lru_cache()
def get_settings():
    """
    caches a config.Settings instance for
    - accessing environmental variables
    - db user + pw
    - etc
    """
    return config.Settings()


async def valid_content_length(content_length: int = Header(..., lt=12_000)):
    """
    Defines the maximum size of content allowed as sent by the header. Does not prevent client sending invalid header.
    """
    return content_length


# TODO: refactor NAS to be an alternate 'localhost' file store
async def get_nas():
    nas = "NAS"
    yield nas


async def get_user_db():
    """"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_images_db():
    """"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_thumbs_nas():
    nas = "thumbnails"
    yield nas