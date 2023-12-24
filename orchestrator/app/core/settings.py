from pydantic import AmqpDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_DSN: AmqpDsn


settings = Settings()
