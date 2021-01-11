from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy_utils import URLType
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


from .database import DB_PROVIDER #TODO: migrate to postgres instead of sqllite and fix date_created default time accordingly

# many to many images:tags
images_tags_association = Table('image_tags', Base.metadata,
    Column('image_id', Integer, ForeignKey('images.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) #pk

    date_created = Column(DateTime, server_default=func.now()) if DB_PROVIDER == 'PG' else Column(DateTime,server_default = func.datetime('now')) #sqllite has no now(), postgres does this is a long long line
    #https://www.techonthenet.com/sqlite/functions/now.php
    # ternary operator: a if condition else b

    hashed_password = Column(String) #hashed
    username = Column(String, unique = True)
    permission_lvl = Column(Integer)
    disabled = Column(Boolean, default = False)


    image = relationship("Image", back_populates="owner") #maintains referential

    class Config:
        orm_mode = True



class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, server_default=func.now()) if DB_PROVIDER == 'PG' else Column(DateTime,server_default = func.datetime('now')) #sqllite has no now(), postgres does this is a long long line


    hash = Column(String) # used for constructing url to NAS --> TODO: consider hash collisions at enormous amounts of images
    url = Column(URLType)
    url_thumb = Column(URLType) #need to create

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="image")

    tags = relationship(
        "Tag",
        secondary=images_tags_association,
        back_populates="images")
    
    class Config:
        orm_mode = True


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, server_default=func.now()) if DB_PROVIDER == 'PG' else Column(DateTime,server_default = func.datetime('now')) #sqllite has no now(), postgres does this is a long long line

    title = Column(String(length=255))

    images = relationship(
        "Image",
        secondary=images_tags_association,
        back_populates="tags")

    class Config:
        orm_mode = True



    