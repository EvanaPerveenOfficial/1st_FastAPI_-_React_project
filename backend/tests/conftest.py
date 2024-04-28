import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.sqlalchemy_models import Base
from unittest.mock import patch

from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


Dummy_URL_DATABASE = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/dummy"
dummy_engine = create_engine(Dummy_URL_DATABASE)
Dummy_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=dummy_engine)
Dummy_Base = declarative_base()


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


@pytest.fixture(scope="session", autouse=True)
def drop_tables_after_test_session(request, test_db):
    def drop_tables():
        Base.metadata.drop_all(bind=dummy_engine)

    request.addfinalizer(drop_tables)