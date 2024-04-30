import asyncio
from fastapi import status
from app.models.sqlalchemy_models import User
from app.utils import async_hash_password
import uuid
from unittest.mock import patch

@patch("app.routers.auth_user.get_db")
def test_create_user(mock_get_db, test_client):
    email = f"user_{uuid.uuid4()}@example.com"
    password = "password"
    role = "user"

    db_session_mock = mock_get_db.return_value

    async def async_create_user(db_session, email, password, role):
        return {"email": email}

    mock_create_user = patch("app.routers.auth_user.create_user", return_value=async_create_user)


    with mock_create_user:
        response = test_client.post(
            "/auth/create-user", data={"email": email, "password": password, "role": role}
        )

    assert response.status_code == 201
    user_data = response.json()
    assert user_data["email"] == email



