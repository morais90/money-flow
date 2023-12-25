from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DSN: PostgresDsn = "postgresql+asyncpg://postgres:moneyflow@postgres:5432/moneyflow"


settings = Settings()
