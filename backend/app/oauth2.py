from jose import JOSEError, jwt
from datetime import datetime, timedelta
from app.schemas.auth_models import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()

bearer_scheme = HTTPBearer()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get('user_id'))
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except JOSEError:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(bearer_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={'WWW-Authenticate': 'Bearer'})
    return verify_access_token(token.credentials, credential_exception)
