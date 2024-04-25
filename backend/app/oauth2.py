from jose import jwt
from datetime import datetime, timedelta
from app.schemas.auth_models import TokenData
from fastapi import Depends, status, HTTPException, Cookie
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()

bearer_scheme = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_data(
    token: str = Cookie(None),
) -> TokenData:
    # token = request.cookies.get("access_token")
    # print("token: ", token)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = str(payload.get("user_id"))
        # print(id)
        role = str(payload.get("role"))
        if not id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(id=id, role=role)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: TokenData = Depends(get_token_data)):
    return token.id


def get_current_user_role(token_data: TokenData = Depends(get_token_data)):
    return token_data.role
