import datetime
from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    image_url: Optional[str]
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class Cart(BaseModel):
    items: List[Product]

    class Config:
        from_attributes = True


class Order(BaseModel):
    products: List[Cart]

    class Config:
        from_attributes = True

