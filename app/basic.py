from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import FastAPI,Response,HTTPException,status,Depends
from psycopg2.extras import RealDictCursor
import time
from app.config import settings
import psycopg2
from app import models
from sqlalchemy.orm import session
from app.database import get_db,engine
from .import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Product(BaseModel):
    name: str
    price: int
    availbale: bool = True 
    inventory: int = 0


while True:
    try:
        conn = psycopg2.connect(
            host=settings.database_hostname,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            port=settings.database_port,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("database connection OK")
        break
    except Exception as error:
        print("database connection failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [
    {"title":"title of post 1","content":"contenet of contnet 1","id":1},
    {"title":"favourite foods","content":"i love birani with sprite","id":2}
]

def find_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i;

def search_post(post_id: int): 
    for p in my_posts:
        if p['id'] == post_id:  
            return p
    return None

@app.get("/sqlalchemy")
def posts(db:session = Depends(get_db)):
    post = db.query(models.Product)
    print(post)
    return {"status":"succesfull"}

@app.get("/")
def root():
    return {"hello":"world"}

@app.get("/posts")
def get_posts(db:session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM products""")
    #posts = cursor.fetchall()
    post = db.query(models.Product).all()
    return {"data":post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_product(product: Product,db:session = Depends(get_db)):
    #cursor.execute(
        #"""INSERT INTO products (name, price, availbale, inventory) 
           #VALUES (%s, %s, %s, %s) RETURNING *""",
        #(product.name, product.price, product.availbale, product.inventory)
    #)
    #new_product = cursor.fetchone()
    #conn.commit()
    new_post = models.Product(name = product.name,price = product.price,inventory = product.inventory)
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):  
    cursor.execute("""select * from products where id = %s""",(str(id)))
    post = cursor.fetchone()
    post = search_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found :(")
    return {"post detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM products WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with this id:{id} not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@app.put("/posts/{id}")
def update_post(id: int, post: Product):
    cursor.execute(
        """UPDATE products SET name = %s, price = %s, availbale = %s, inventory = %s WHERE id = %s RETURNING *""",
        (post.name, post.price, post.availbale, post.inventory, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with this id:{id} not found")
    
    return {"data": updated_post}