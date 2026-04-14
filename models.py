from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Products (Base):
    __tablename__ = "Products"

    id_product = Column(Integer, primary_key=True, index=True)
    product = Column(String(100), nullable=False, unique=True)
    stock = Column(Integer, default=0)
    price = Column(Numeric(10,2), nullable=False)
    description = Column(String(250))
    image = Column(String)
    id_category = Column(Integer, ForeignKey("Category.id_category"))
    date_exp = Column(Date, nullable=True)

    categoria = relationship("Category", back_populates="productos")

class Category (Base):
    __tablename__ = "Category"

    id_category = Column(Integer, primary_key=True,index=True)
    category = Column(String(100), unique=True)

    productos = relationship("Products", back_populates="categoria")