import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    image_url: Optional[str]
    created_at: datetime.datetime

    ConfigDict: Dict[str, bool] = {"allow_mutation": False}


class Cart(BaseModel):
    items: List[Product]

    ConfigDict: Dict[str, bool] = {"allow_mutation": False}


class Order(BaseModel):
    products: List[Cart]

    ConfigDict: Dict[str, bool] = {"allow_mutation": False}
