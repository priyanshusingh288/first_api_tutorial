from fastapi import FastAPI,HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.params import Body

app = FastAPI()

items = []

@app.get("/")
def root():
    return {"hello":"world"}

@app.post("/items")
def create_items(item:str):
    items.append(item)
    print(items)
    return items

@app.get("/items")
def list_limits(limit:int = 10):
    print(limit)
    return items[0:limit]

@app.get("/items/{item_id}")
def get_items(item_id:int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail = "item not found")
    
