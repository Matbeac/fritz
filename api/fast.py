from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import pickle
import numpy as np
import json
import tensorflow as tf
import os
from tensorflow import keras
from fritz.utils import load_model, load_classes

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

# model_path= os.path.join('..','models/10_VGG16.h5')
model_path='/home/mateo/code/Matbeac/fritz/models/10_86_7_DN121_AUG_TV_ES5_RLR1_TL2_ES5_RLR1_TL3.h5'
classes_path= '/home/mateo/code/Matbeac/fritz/models/10_VGG16.csv'
model = load_model(model_path)

@app.post("/predict")
async def predict(image:Item):
    # Get the image from the upload
    response = np.array(json.loads(image.image_reshape))
    response_reshape=response.reshape((image.height,image.width,image.color))    
    
    # Resize the image ⚠ WITHOUT PAD
    response_reshape = tf.image.resize(response_reshape,[224, 224])
    
    # Load the model
    probabilities=model.predict(np.array([response_reshape/255]))
    index=np.argmax(probabilities)
    recipe = load_classes(classes_path,index)
    return recipe
    

@app.post("/items/")
async def create_item(item: Item):
    response = np.array(json.loads(item.image_reshape))
    response_reshape=response.reshape((item.height,item.width,item.color))
    filehandler = open(b"Image.obj","wb")
    pickle.dump(response_reshape,filehandler)
    return "item"