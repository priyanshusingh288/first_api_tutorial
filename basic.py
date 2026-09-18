from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import FastAPI,Response,HTTPException,status
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Product(BaseModel):
    name: str
    price: int
    availbale: bool = True  
    inventory: int = 0

while True:
 try:
    conn = psycopg2.connect(host = "localhost",database = "fastapi",user = "postgres",password = 'S1g2m3@pri' , cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connected succesfully")
    break
 except Exception as error:
    print("database connection unsuccesfull")
    print("error : ",error)
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

@app.get("/")
def root():
    return {"hello":"world"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM products""")
    posts = cursor.fetchall()
    print(posts)
    return {"this is your ": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    cursor.execute(
        """INSERT INTO products (name, price, availbale, inventory) 
           VALUES (%s, %s, %s, %s) RETURNING *""",
        (product.name, product.price, product.availbale, product.inventory)
    )
    new_product = cursor.fetchone()
    conn.commit()
    return {"data": new_product}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):  
    cursor.execute("""select * from products where id = %s""",(str(id)))
    post = cursor.fetchone()
    post = search_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with id {id} not found :(")
    return {"post detail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id:{id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Product):
    cursor.execute("""UPDATE post set name = %s,price = %s,available = %s,inventory = %s RETURNING *""",
                    (post.name, post.price, post.availbale, post.inventory))
    updated_post = cursor.fetchone
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id:{id} not found")
        return {"data":updated_post}

    
