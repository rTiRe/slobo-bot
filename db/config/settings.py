from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    RABBIT_HOST: str
    RABBIT_PORT: int
    RABBIT_DEFAULT_USER: str
    RABBIT_DEFAULT_PASS: str
    RABBIT_WEB_PORT: int

    # USER_GIFT_QUEUE_TEMPLATE: str = 'user_gifts.{user_id}'

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@bot_postgres:5432/{self.DB_NAME}"

    @property
    def rabbit_url(self) -> str:
        return f"amqp://{self.RABBIT_DEFAULT_USER}:{self.RABBIT_DEFAULT_PASS}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"

    class Config:
        env_file = "config/.env"


settings = Settings()