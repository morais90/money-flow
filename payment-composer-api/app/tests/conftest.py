import pendulum
import pytest
from fastapi.testclient import TestClient

from app.core.models import Model
from app.main import app

from .database import create_database, engine


@pytest.fixture(scope="session", autouse=True)
def freeze_time():
    known = pendulum.datetime(2023, 12, 24, 12, tz="UTC")
    pendulum.set_test_now(known)


@pytest.fixture(scope="session", autouse=True)
def create_db():
    create_database()

    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)


@pytest.fixture
def client():
    return TestClient(app)
