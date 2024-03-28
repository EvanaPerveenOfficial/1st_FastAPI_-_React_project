from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional


class UserCreate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime
    
    class Config:
        from_attributes = True
        
        
        
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True
        
        
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        from_attributes = True
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    class Config:
        from_attributes = True