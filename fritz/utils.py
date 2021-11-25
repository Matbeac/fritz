import tensorflow
from tensorflow import keras
import pandas as pd

def load_model(model_path):
    model = keras.models.load_model(model_path)
    return model

def load_classes(classes_path,index):
    classes=pd.read_csv(classes_path)
    return classes.iloc[index,0]
