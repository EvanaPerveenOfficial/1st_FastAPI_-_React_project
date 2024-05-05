import json

from fastapi import APIRouter, Depends, Form, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.sqlalchemy_models import User
from app.oauth2 import create_access_token
from app.schemas.auth_models import UserInResponse
from app.utils import async_hash_password, verify_password

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
    db: AsyncSession = Depends(get_db),
):
    try:
        print(f"Received email: {email}, password: {password}, role: {role}")

        existing_user = await db.execute(select(User).where(User.email == email))
        if existing_user.scalar():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )
        hashed_password = await async_hash_password(password)

        user_data = {"email": email, "password": hashed_password, "role": role}
        user = User(**user_data)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )


@router.get(
    "/user/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Authentication"],
    response_model=UserInResponse,
)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.get(User, id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} does not exist",
            )
        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}",
        )


@router.post("/login", status_code=status.HTTP_200_OK, tags=["Authentication"])
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await db.execute(select(User).filter(User.email == email))
        user = user.scalar_one()

        print("Retrieved user:", user)

        if not user or not verify_password(password, user.password):
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
            max_age=1800,
        )
        return response

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log in: {str(e)}",
        )
