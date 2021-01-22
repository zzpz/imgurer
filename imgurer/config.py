from fastapi import FastAPI
from pydantic import BaseSettings
from os import getenv


class Settings(BaseSettings):
    app_name: str = getenv("APP_NAME", "imgurer")
    admin_email = getenv("ADMIN_EMAIL", "admin@url.io")

    WEED_MASTER_URL: str = getenv("WEED_MASTER_URL", "http://localhost:9333")
    # WEED_MASTER_URL: str  # seaweedFS
    # WEED_VOLUME_URL: str = "localhost:8080"  # don't need?

    SECRET_KEY: str = getenv(
        "SECRET_KEY", "areallylongstringofnumbersandcharactersformakingtokens1234567890"
    )
    ALGORITHM: str = getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 25)

    # TODO: understand why python-dotenv can't find the .env file
    # replace os.getenv() calls

    # with open("../.env", "r") as fh:
    #   print(fh.read)

    # class Config:
    #     env_prefix = ""
    #     env_file = "../.env"


class DatabaseSettings(Settings):
    """
    Future work to decouple settings from one large class
    """

    DB_URL: str = getenv("DB_URL", "sqlite:///./sql_app.db")
    DB_PROVIDER: str = "Elephant"


settings = Settings()