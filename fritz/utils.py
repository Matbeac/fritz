import os
import tensorflow
from tensorflow import keras
import pandas as pd
import requests
import pandas as pd
import collections
from dotenv import load_dotenv, find_dotenv

def load_model(model_path):
    model = keras.models.load_model(model_path)
    return model

def load_classes(classes_path,index):
    classes=pd.read_csv(classes_path)
    return classes.iloc[index,0]

# Fetch credentials
env_path = join(dirname(dirname(__file__)), '.env')  # ../.env
env_path = find_dotenv()  # automatic find
load_dotenv(env_path)
api_key_rapidapi = os.getenv("RAPIDAPI_MATEO_KEY")

def recipes_call(dish, food_type, results_number=20):

    # first call --> getting the recipes for a dish
    get_id_url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    id_querystring = {f"query":{dish},"number":{results_number}, "type":{food_type}}
    id_headers = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": api_key_rapidapi
        }
    get_id_response = requests.request("GET", get_id_url, headers=id_headers, params=id_querystring)

    recipes = get_id_response.json()["results"]

    return recipes

def get_id(dish, food_type, results_number=20):

    recipes = recipes_call(dish, food_type, results_number)
    # recipes' titles
    titles = [[i][0]["title"] for i in recipes]

    # choosing just one recipe
    for title in titles:
        if dish in title.lower() and len(title) < len(dish)+15:
            break

    # recipe index
    index = titles.index(title)
    #number of serving to calculate a portion
    servings = recipes[index]["servings"]
    # recipe id for second call
    recipe_id = recipes[index]["id"]

    return servings, recipe_id

def id_call(dish, food_type, results_number=20):

    serving, recipe_id = get_id(dish, food_type, results_number)
    # second call --> getting the ingredintes of a recipe
    get_recipe_url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/ingredientWidget.json"
    recipe_headers = {
        "x-rapidapi-host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "x-rapidapi-key": api_key_rapidapi
        }
    get_recipe_response = requests.request("GET", get_recipe_url, headers=recipe_headers)

    ingredients = get_recipe_response.json()["ingredients"]

    return ingredients

def create_ingredients_dict(dish, food_type, results_number = 20):

    ingredients = id_call(dish, food_type, results_number)
    servings = get_id(dish, food_type, results_number)[0]

    # creating the dictionary with all the ingredients/metrics/values
    keys = ["name", "amount"]
    ingredients_dict = collections.defaultdict(list)

    for i in ingredients:
        new_dic = {k: i[k] for k in i.keys() & keys}
        metrics = new_dic["amount"]["metric"]["unit"]
        values = new_dic["amount"]["metric"]["value"]
        ingredients_dict["ingredient"].append(i["name"])
        ingredients_dict["value"].append(round(values / servings, 2))
        ingredients_dict["metric"].append(metrics)

    return ingredients_dict
