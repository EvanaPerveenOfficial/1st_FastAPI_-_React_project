from fastapi import APIRouter, HTTPException, Depends, status, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sqlalchemy_models import Product
from app.schemas.models import Product as ProductSchema
from app.oauth2 import get_current_user_role

router = APIRouter()


def admin_check(user_role: str = Depends(get_current_user_role)):
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


@router.post(
    "/products/",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
    description="Create a new product",
)
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    image_url: str = Form(...),
    db: Session = Depends(get_db),
    admin: None = Depends(admin_check),
):
    product = Product(
        name=name, description=description, price=price, image_url=image_url
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/products/", response_model=list[ProductSchema], tags=["Products"])
def read_products(
    skip: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
):
    products = db.query(Product).order_by(Product.id).offset(skip).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.put("/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def update_product(
    product_id: int,
    product: ProductSchema,
    db: Session = Depends(get_db),
    admin: None = Depends(admin_check),
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", tags=["Products"])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: None = Depends(admin_check),
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
