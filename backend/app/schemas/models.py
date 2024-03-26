from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    image_url: Optional[str]

    class Config:
        orm_mode = True


class Cart(BaseModel):
    items: List[Product]

    class Config:
        orm_mode = True


class Order(BaseModel):
    products: List[Cart]

    class Config:
        orm_mode = True
