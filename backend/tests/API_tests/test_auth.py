from app.routers.auth_user import create_access_token
from fastapi import status



def test_create_user(test_client, db_session):
    email = "test@example.com"
    password = "testpassword"
    role = "admin"

    response = test_client.post(
        "/auth/create-user", data={"email": email, "password": password, "role": role}
    )

    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}"


def test_create_access_token():
    user_id = 1
    role = "user"
    access_token = create_access_token(data={"user_id": user_id, "role": role})
    assert isinstance(access_token, str)
    assert access_token != ""


def test_login_success(test_client):
    email = "test@example.com"
    password = "testpassword"

    response = test_client.post(
        "/auth/login", data={"email": email, "password": password}
    )

    assert response.status_code == 200
    assert "token" in response.cookies
    assert response.json() == {"Status": "Successfully Logged In!!!"}


def test_login_invalid_credentials(test_client):
    email = "nei@gmail.com"
    password = "invalidpass"

    response = test_client.post(
        "/auth/login", data={"email": email, "password": password}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"


def test_get_user_existing(test_client, db_session):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
        "role": "admin",
    }
    response = test_client.get("/auth/user/1")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["email"] == user_data["email"]


def test_get_user_non_existing(test_client):
    response = test_client.get("/auth/user/10000")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User with id: 10000 does not exist"
