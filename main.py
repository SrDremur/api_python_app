from typing import Annotated
from fastapi import FastAPI, Form, UploadFile, Depends, Body
from datetime import date
from sqlalchemy.orm import Session
from database import get_db, engine
import category_validate
import models, schemas
from database import get_db

app = FastAPI()

@app.get("/categories/{id_cat}")
async def read_category (id_cat:int,db:Session = Depends(get_db)):
    
    category = db.query(models.Category).filter(models.Category.id_category == id_cat).first()

    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return category

@app.get("/categories")
async def read_categories(db:Session = Depends(get_db)):
    
    categorias = db.query(models.Category).all()

    return categorias

@app.post("/categories", response_model=schemas.Category)
async def upload_category(category_data : schemas.CategoryCreate, db : Session = Depends(get_db)):
    
    new_category = models.Category(
        category = category_data.category
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.put("/categories/{id_category}")
async def update_category (id_category:int,category:str = Body(...,embed=True),db:Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id_category == id_category).first()

    if not db_category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    db_category.category = category

    db.commit()
    db.refresh(db_category)

    return db_category

@app.delete("/categories/{id_category}")
async def delete_category (id_category:int, db:Session = Depends(get_db)):
    
    db_category = db.query(models.Category).filter(models.Category.id_category == id_category).first()

    if not db_category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    
    db.delete(db_category)
    db.commit()

    return {"message": "Categoria eliminada con exito"}

@app.get("/products/{id_pro}")
async def read_product (id_pro:int, db: Session = Depends(get_db)):

    product = db.query(models.Products).filter(models.Products.id_product == id_pro).first()

    if not product:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Producto sin existencia")
    
    return product

@app.get("/products")
async def read_products(db:Session = Depends(get_db)):
    products=db.query(models.Products).all()
    return products

@app.post("/products",response_model=schemas.Product)
async def upload_product(product_data:schemas.ProductCreate,db:Session = Depends(get_db)):
    new_product=models.Products(
        product=product_data.product,
        stock=product_data.stock,
        price=product_data.price,
        description=product_data.description,
        id_category=product_data.id_category,
        date_exp=product_data.date_exp
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.put("/products/{product_id}")
async def update_product(product_id:int,product:str = Body(...,embed=True), stock:int = Body(...,embed=True), price: float = Body(...,embed=True), description: str = Body(embed=True), id_category: int = Body(...,embed=True), date_exp: date = Body(...,embed=True), db:Session = Depends(get_db)):

    db_product = db.query(models.Products).filter(models.Products.id_product == product_id).first()

    if not (db_product):
        from fastapi import HTTPException
        raise HTTPException(status_code=404,detail="El producto no existe")
    
    db_product.product = product
    db_product.stock = stock
    db_product.price = price
    db_product.description = description
    db_product.id_category = id_category
    db_product.date_exp = date_exp

    db.commit()
    db.refresh(db_product)
    
    return db_product

@app.delete("/products/{product_id}")
async def delete_product(product_id:int,db:Session = Depends(get_db)):
    db_product = db.query(models.Products).filter(models.Products.id_product == product_id).first()

    if not (db_product):

        from fastapi import HTTPException
        raise HTTPException(status_code=404,detail="El producto no existe")
    
    db.delete(db_product)
    db.commit()
    return {"mensaje":"Producto eliminado con exito"}
