from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Product
from database import session, engine
import databasemodels

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

databasemodels.Base.metadata.create_all(bind=engine)


products = [
    Product(id=1, name="Laptop", price=999, quantity=10, description="A high-performance laptop for all your computing needs."),
    Product(id=2, name="Smartphone", price=499, quantity=20, description="A sleek and powerful smartphone for your daily use."),
]

#closing the db connection
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


#@app.get("/products")
# def get_products():
#     #db connection
#     db = session()
#     db.query()

#     return products

#depedency injection for db connection
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(databasemodels.Product).all()
    return db_products


#for adding columns to the database
def init_db():
    db = session()
    #it should add the data to db  only when table is empty
    count = db.query(databasemodels.Product).count()
    if count == 0:
        for product in products:
            db.add(databasemodels.Product(**product.model_dump()))
        db.commit()

init_db()


#GET: fetch a product by id
@app.get("/products/{id}")
def get_product_by_id(id:int, db:Session = Depends(get_db)):
    db_product = db.query(databasemodels.Product).filter(databasemodels.Product.id == id).first()
    if db_product:
        return db_product
    #for product in products:
       # if product.id == id:
           # return product
    return {"error": "Product not found"}

@app.get("/")
def greet(): 
    return "welcome to the world of programming!"

@app.get("/bake")
def bake(): 
    return "welcome to the world of baking!"

@app.get("/cook")
def cook(): 
    return "welcome to the world of cooking!"

#POST: add a new product/submit a new product
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    #products.append(product)
    #return product
    db.add(databasemodels.Product(**product.model_dump()))
    db.commit()
    return product   

#PUT : update the data
@app.put("/products/{id}")
def update_product(id:int , product: Product, db:Session = Depends(get_db)):
        db_product = db.query(databasemodels.Product).filter(databasemodels.Product.id == id).first()
        if db_product:
            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            db.commit()
            return "Product Updated" 

        else:
            return "No Product found"
    #for i in range(len(products)):
     #   if products[i].id == id:
      #      products[i] = product
       #     return "Product updated successfully"
    #return {"error": "Product not found"}

#DELETE: delete a product 
@app.delete("/products/{id}")
def delete_product(id:int, db:Session = Depends(get_db)):
    db_product = db.query(databasemodels.Product).filter(databasemodels.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "Product not found"
    #for i in range(len(products)):
     #   if products[i].id == id:
      #      del products[i]
       #     return "Product deleted successfully"
    #return {"error": "Product not found"}



 