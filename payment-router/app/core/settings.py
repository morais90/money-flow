from pydantic import AmqpDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PAYMENT_COMPOSER_API: str
    RABBITMQ_DSN: AmqpDsn


settings = Settings()
