from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str

    MAIL_FROM: str
    


    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()


