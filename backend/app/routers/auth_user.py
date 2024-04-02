from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sqlalchemy_models import User
from app.schemas.auth_models import UserCreate
from fastapi import Form
from app.utils import hash_password, verify_password
from ..oauth2 import create_access_token
import json


router = APIRouter()




@router.post('/create-user', status_code=status.HTTP_201_CREATED, tags=['Authentication'], response_model=UserCreate)
def create_user(email: str = Form(...), password: str = Form(...),role: str = Form(...) , db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = hash_password(password)
    user_data = {'email': email, 'password': hashed_password, 'role': role}
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user 

@router.get('/user/{id}', status_code=status.HTTP_200_OK, tags=['Authentication'], response_model=UserCreate)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    return user





@router.post('/login', status_code=status.HTTP_202_ACCEPTED, tags=['Authentication'])
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"user_id": user.id})
    
    response_content = {'token_type': 'bearer', 'role': user.role, 'token': access_token}
    
    response = Response(content=json.dumps(response_content), media_type='application/json')
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite='lax', 
        max_age=1800,
    )
    
    return response


