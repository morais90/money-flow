from app.core.database import Session


async def get_session() -> Session:
    try:
        yield Session()
    finally:
        await Session.remove()
