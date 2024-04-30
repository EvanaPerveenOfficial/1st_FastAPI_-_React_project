import asyncio
import uuid
from unittest.mock import MagicMock, patch
from fastapi import status
from app.models.sqlalchemy_models import User
from app.routers.auth_user import get_user, login


@patch("app.routers.auth_user.get_db")
def test_create_user(mock_get_db, test_client):
    email = f"user_{uuid.uuid4()}@gmail.com"
    password = "password"
    role = "user"

    async def async_create_user(db_session, email, password, role):
        return {"email": email}

    mock_create_user = patch(
        "app.routers.auth_user.create_user", return_value=async_create_user
    )

    with mock_create_user:
        response = test_client.post(
            "/auth/create-user",
            data={"email": email, "password": password, "role": role},
        )

    assert response.status_code == 201
    user_data = response.json()
    assert user_data["email"] == email


@patch("app.routers.auth_user.get_db")
def test_get_user(mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_user = User(id=1, email="test@gmail.com")
    mock_db_session.query().filter().first.return_value = mock_user

    response = asyncio.run(get_user(id=1, db=mock_db_session))

    assert response.email == "test@gmail.com"


@patch("app.routers.auth_user.get_db")
@patch("app.routers.auth_user.verify_password")
@patch("app.routers.auth_user.create_access_token")
def test_login(mock_create_access_token, mock_verify_password, mock_get_db):
    mock_db_session = MagicMock()
    mock_get_db.return_value = mock_db_session
    mock_user = User(
        email="unittest@gmail.com", password="hashed_password", role="user"
    )
    mock_db_session.query().filter().first.return_value = mock_user

    mock_verify_password.return_value = True

    mock_create_access_token.return_value = "dummy_access_token"

    response = login(
        email="unittest@gmail.com", password="password", db=mock_db_session
    )

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.headers["Set-Cookie"]
