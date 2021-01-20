from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import getenv


# SQLALCHEMY_DATABASE_URL = postgres://USER:PASSWORD@SERVER:PORT/database
SQLALCHEMY_DATABASE_URL = getenv("DB_URL")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # false for sqlite reasons
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()