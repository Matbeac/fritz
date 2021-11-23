from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
def index():
    return {"greeting": "Hello world"}

class Item(BaseModel):
    image_reshape: str
    height:int
    width:int
    color:int

@app.post("/items/")
async def create_item(item: Item):
    str_np = item.image_reshape
    return item