from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sqlalchemy_models import Product
from app.schemas.models import Product as ProductSchema
from app.oauth2 import get_current_user
from fastapi import Form

router = APIRouter()



@router.post("/products/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED, tags=['Products'])
def create_product(name: str = Form(...), description: str = Form(...), price: int = Form(...), image_url: str = Form(...), 
                   db: Session = Depends(get_db), 
                   user_id: int = Depends(get_current_user)):
    product_data = {"name": name, "description": description, "price": price, "image_url": image_url}
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product




@router.get("/products/", response_model=list[ProductSchema], tags=['Products'])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  user_id: int = Depends(get_current_user)):
    products = db.query(Product).order_by(Product.id).offset(skip).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=ProductSchema, tags=['Products'])
def read_product(product_id: int, db: Session = Depends(get_db), 
    user_id: int = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=ProductSchema, tags=['Products'])
def update_product(product_id: int, product: ProductSchema, db: Session = Depends(get_db),
                   user_id: int = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.image_url = product.image_url

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", tags=['Products'])
def delete_product(product_id: int, db: Session = Depends(get_db),
                   user_id: int = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

