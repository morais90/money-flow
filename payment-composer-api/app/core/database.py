from asyncio import current_task

from app.core.settings import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.POSTGRES_DSN, echo=True, connect_args={"server_settings": {"jit": "off"}}
)
async_session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)
Session = async_scoped_session(async_session_factory, scopefunc=current_task)

Base = declarative_base()
