from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Product

router = APIRouter()

cart_items = []


@router.post("/cart/add/", response_model=List[Product])
def add_to_cart(product: Product):
    cart_items.append(product)
    return cart_items


@router.get("/cart/", response_model=List[Product])
def view_cart():
    return cart_items


@router.delete("/cart/remove/{product_id}", response_model=List[Product])
def remove_from_cart(product_id: int):
    global cart_items
    cart_items = [p for p in cart_items if p.id != product_id]
    return cart_items
