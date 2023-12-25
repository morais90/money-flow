from app.core.database import Session, engine


async def get_session() -> Session:
    session = Session()

    try:
        yield session
    finally:
        await session.close()
        await engine.dispose()
