import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.sqlalchemy_models import Base
from unittest.mock import patch
from dotenv import load_dotenv
import os


load_dotenv()

DB_DATABASE = os.getenv("DB_DATABASE")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_DATABASE}.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def in_memory_db():
    memory_engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=memory_engine)
    yield memory_engine
    Base.metadata.drop_all(bind=memory_engine)
    memory_engine.dispose()


TestingSessionInMemory = sessionmaker(autocommit=False, autoflush=False)


@pytest.fixture
def in_memory_session(in_memory_db):
    db = TestingSessionInMemory(bind=in_memory_db)
    try:
        yield db
    finally:
        db.close()


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
