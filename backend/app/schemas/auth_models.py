from pydantic import BaseModel, EmailStr
import datetime
# from typing import List, Optional


class UserCreate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime
    

    class Config:
        from_attributes = True
        
        