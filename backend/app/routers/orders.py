from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Product

router = APIRouter()

@router.post("/order/", response_model=List[Product])
def place_order():
    global cart_items
    if not cart_items:
        raise HTTPException(status_code=400, detail="Add products to cart first.")
    ordered_items = cart_items.copy()
    cart_items = []
    return ordered_items
