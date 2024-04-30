import json
from fastapi import APIRouter, Depends, HTTPException, Response, status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sqlalchemy_models import User
from app.schemas.auth_models import UserCreate, UserInResponse
from app.utils import async_hash_password, verify_password
from app.oauth2 import create_access_token


router = APIRouter()


@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    response_model=UserInResponse,
)
async def create_user(
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    hashed_password = await async_hash_password(password)
    user_data = {"email": email, "password": hashed_password, "role": role}
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "/user/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
    response_model=UserInResponse,
)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user


@router.post("/login", status_code=status.HTTP_200_OK, tags=["Authentication"])
def login(
    email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = create_access_token(data={"user_id": user.id, "role": user.role})

    response_content = {"Status": "Successfully Logged In!!!"}

    response = Response(
        content=json.dumps(response_content), media_type="application/json"
    )

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        # secure=True,
        max_age=1800,
    )

    return response
