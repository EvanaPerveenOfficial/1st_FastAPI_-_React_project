from app.routers.auth_user import create_access_token

import uuid

def test_create_user(test_client, db_session):
    # Generate a unique email address using UUID
    email = f"test_{uuid.uuid4()}@gmail.com"
    password = "testpassword"
    role = "user"
    
    response = test_client.post("/auth/create-user", data={"email": email, "password": password, "role": role})

    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        
        
def test_create_access_token():
    user_id = 1
    role = "user"
    access_token = create_access_token(data={"user_id": user_id, "role": role})
    assert isinstance(access_token, str)
    assert access_token != ""
    
    

def test_login_success(test_client):
    email = 'test@example.com'
    password = "testpassword"

    response = test_client.post("/auth/login", data={"email": email, "password": password})

    assert response.status_code == 200 
    assert "token" in response.cookies
    assert response.json() == {"Status": "Successfully Logged In!!!"}


def test_login_invalid_credentials(test_client):
    email = "nei@gmail.com"
    password = "invalidpass"
    
    response = test_client.post("/auth/login", data={"email": email, "password": password})
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid Credentials"
