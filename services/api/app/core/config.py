from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Подключение к PostgreSQL
    DATABASE_URL: str

    # Redis внутри Docker Compose
    REDIS_URL: str = "redis://redis:6379/0"

    # Обязательный секрет из переменной окружения или .env
    SECRET_KEY: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()