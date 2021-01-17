from fastapi import Header
from .database import SessionLocal


async def valid_content_length(content_length: int = Header(..., lt=12_000)):
    """
    Defines the maximum size of content allowed as sent by the header. Does not prevent client sending invalid header.
    """
    return content_length


# a dependency
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