import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from app.core.models import Model
from app.main import app

from .database import create_database, engine


@pytest.fixture(scope="session", autouse=True)
def freeze():
    freezer = freeze_time("2023-12-24 12:00:00")
    freezer.start()

    yield

    freezer.stop()


@pytest.fixture(scope="session", autouse=True)
def create_db():
    create_database()

    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)


@pytest.fixture
def client():
    return TestClient(app)
