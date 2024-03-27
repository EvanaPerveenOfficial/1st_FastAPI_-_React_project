from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.sqlalchemy_models import User
from app.schemas.auth_models import UserCreate
from fastapi import Form
from app.utils import hash_password


router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create-user', status_code=status.HTTP_201_CREATED, tags=['Authentication'], response_model=UserCreate)
def create_user(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = hash_password(password)
    user_data = {'email': email, 'password': hashed_password}
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user 
    



