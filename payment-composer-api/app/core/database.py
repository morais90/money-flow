from asyncio import current_task

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from app.core.settings import settings

engine = create_async_engine(str(settings.POSTGRES_DSN), echo=False, connect_args={"server_settings": {"jit": "off"}})
async_session_factory = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine, class_=AsyncSession
)

Session = async_scoped_session(async_session_factory, scopefunc=current_task)

Base = declarative_base()


async def get_or_create(session, model, defaults=None, **kwargs):
    created = False

    try:
        statement = select(model).filter_by(**kwargs)
        instance = (await session.scalars(statement)).one()

    except NoResultFound:
        kwargs |= defaults or {}
        instance = model(**kwargs)

        session.add(instance)
        await session.commit()

        created = True

    return instance, created


async def create_or_update(session, model, defaults=None, **kwargs):
    instance, created = await get_or_create(session, model, defaults, **kwargs)

    if created:
        return instance

    kwargs |= defaults or {}

    for key, value in kwargs.items():
        setattr(instance, key, value)

    await session.commit()
    return instance
