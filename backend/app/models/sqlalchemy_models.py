from sqlalchemy import Column, ForeignKey, Integer, String, Table
from app.database import Base
from sqlalchemy.orm import relationship

    
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)
    image_url = Column(String, index=True) 
    
    orders = relationship("Order", secondary="order_products", back_populates="products")
    
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url
        }


class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer, primary_key=True, index=True)
    
    orders = relationship("Order", back_populates="cart")


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    
    cart = relationship("Cart", back_populates="orders")
    
    products = relationship("Product", secondary="order_products", back_populates="orders")


order_products = Table('order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)
