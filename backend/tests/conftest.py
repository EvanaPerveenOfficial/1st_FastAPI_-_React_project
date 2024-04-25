import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Dummy_SessionLocal, dummy_engine, get_db
from app.models.sqlalchemy_models import Base
from unittest.mock import patch

from app.oauth2 import get_token_data


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=dummy_engine)
    yield


@pytest.fixture
def db_session(test_db):
    session = Dummy_SessionLocal()
    yield session
    session.close()


@pytest.fixture
def test_client(db_session):
    with TestClient(app) as client:
        client.app.dependency_overrides[get_db] = lambda: db_session
        yield client


@pytest.fixture(autouse=True)
def mock_create_access_token():
    with patch("app.routers.auth_user.create_access_token") as mock:
        mock.return_value = "mocked_access_token"
        yield


@pytest.fixture
def mock_jwt_decode():
    with patch("app.oauth2.jwt.decode") as mock_decode:
        mock_decode.return_value = {"user_id": 1, "role": "admin"}
        yield mock_decode
