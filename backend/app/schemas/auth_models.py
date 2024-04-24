from pydantic import BaseModel, EmailStr
import datetime
from typing import Optional
from typing import Dict


class UserCreate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime
    
    # class Config:
    #     from_attributes = True
    ConfigDict: Dict[str, bool] = {"allow_mutation": False}
        
        
        
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    ConfigDict: Dict[str, bool] = {"allow_mutation": False}
        
        
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
    ConfigDict: Dict[str, bool] = {"allow_mutation": False}
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None
    
    ConfigDict: Dict[str, bool] = {"allow_mutation": False}