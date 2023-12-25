from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine("postgresql://postgres:moneyflow@postgres:5432/test_db", poolclass=StaticPool)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ScopedSession = scoped_session(Session)


def create_database():
    temporary_engine = create_engine("postgresql://postgres:moneyflow@postgres:5432", poolclass=StaticPool)

    with temporary_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        connection.execute(text("DROP DATABASE if exists test_db;"))
        connection.execute(text("CREATE DATABASE test_db;"))
