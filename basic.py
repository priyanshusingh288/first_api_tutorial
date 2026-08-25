from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):  
    tittle: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title":"title of post 1","content":"contenet of contnet 1","id":1},
    {"title":"favourite foods","content":"i love birani with sprite","id":2}
]

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
    return {"this is your ": my_posts}

@app.post("/create_posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest/")
def get_latest_post():
    post = my_posts[len(my-posts)-1]
    return {"detail":post}

@app.get("/posts/{id}")
def get_post(id: int):  
    post = search_post(id)
    print(post)
    return {"post detail": post}
