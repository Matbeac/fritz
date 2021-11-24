from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import pickle
import numpy as np
import json
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
    response = np.array(json.loads(item.image_reshape))
    response_reshape=response.reshape((item.height,item.width,item.color))
    filehandler = open(b"Image.obj","wb")
    pickle.dump(response_reshape,filehandler)
    return "item"