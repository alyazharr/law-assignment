from fastapi import FastAPI,HTTPException,Query
import requests
import datetime
import random
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
dummy_username = "dummy dumb"
dummy_pass = "dumbdumbdumb"

API_KEY = '691af9f63d9d4a7dbfce4bb7bfcac572'
GOOGLE_API_KEY = 'AIzaSyD8MNCCoI5WKERQthaT1wwf2CiDLe4hj5M'
SEARCH_ENGINE_KEY = '64f41a959b7d146d3'

@app.get('/')
async def root():
    return {"Welcome":"Diet People!", "This is":"Alya Azhar Agharid", "And this is":"LAW Tugas 1"}

# randomize the recipes for today
@app.get("/recipes/today-cook")
async def get_modified_data():
    url = f"https://api.spoonacular.com/recipes/random?apiKey={API_KEY}" 

    tag1 = "appetizer"
    tag2 = "main course"
    tag3 = "dessert"
    
    response_appetizer = requests.get(url, params={"tags": tag1, "number": 3}) 
    response_main_course = requests.get(url, params={"tags": tag2, "number": 3}) 
    response_dessert = requests.get(url, params={"tags": tag3, "number": 3})     

    recipes_appetizer = response_appetizer.json()['recipes']
    recipes_main_course = response_main_course.json()['recipes']
    recipes_dessert = response_dessert.json()['recipes']

    morning = {
        "appetizer": {"id":recipes_appetizer[0]["id"], "title":recipes_appetizer[0]['title'], "source":recipes_appetizer[0]['sourceUrl'], "instructions":recipes_appetizer[0]['instructions']},
        "main course": {"id":recipes_main_course[0]["id"], "title":recipes_main_course[0]['title'], "source":recipes_main_course[0]['sourceUrl'], "instructions":recipes_main_course[0]['instructions']},
        "appetizer": {"id":recipes_dessert[0]["id"], "title":recipes_dessert[0]['title'], "source":recipes_dessert[0]['sourceUrl'], "instructions":recipes_dessert[0]['instructions']}

    }
    noon = {
        "appetizer": {"id":recipes_appetizer[1]["id"], "title":recipes_appetizer[1]['title'], "source":recipes_appetizer[1]['sourceUrl'], "instructions":recipes_appetizer[1]['instructions']},
        "main course": {"id":recipes_main_course[1]["id"], "title":recipes_main_course[1]['title'], "source":recipes_main_course[1]['sourceUrl'], "instructions":recipes_main_course[1]['instructions']},
        "appetizer": {"id":recipes_dessert[1]["id"], "title":recipes_dessert[1]['title'], "source":recipes_dessert[1]['sourceUrl'], "instructions":recipes_dessert[1]['instructions']}

    }
    evening = {
        "appetizer": {"id":recipes_appetizer[2]["id"], "title":recipes_appetizer[2]['title'], "source":recipes_appetizer[2]['sourceUrl'], "instructions":recipes_appetizer[2]['instructions']},
        "main course": {"id":recipes_main_course[2]["id"], "title":recipes_main_course[2]['title'], "source":recipes_main_course[2]['sourceUrl'], "instructions":recipes_main_course[2]['instructions']},
        "appetizer": {"id":recipes_dessert[2]["id"], "title":recipes_dessert[2]['title'], "source":recipes_dessert[2]['sourceUrl'], "instructions":recipes_dessert[2]['instructions']}
    }
    return {"morning":morning, "noon":noon, "evening":evening}

# searching recipes by query and country
@app.get("/recipes/{query}/{cuisine}")
async def search_recipes(query:Optional[str]=None, cuisine:Optional[str]=None):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}" 
    query_params = {"query": query, "cuisine": cuisine} 
    
    response = requests.get(url, params=query_params) 
    return response.json()

# what's in my fridge?
@app.get("/recipes/{ingredients}")
async def whats_in_my_fridge(ingredients: str = Query(None)):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={API_KEY}"
    ingre = ingredients.split('%2C') if ingredients else []
    query_params = {"ingredients": ingre, "ignorePantry":True} 
    response = requests.get(url, params=query_params) 
    return response.json()

# mengambil berbagai jenis quotes 
@app.get('/quotes/{query}')
async def search_google2(query:str):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        search_query = f"site:brainyquote.com {query}-quotes"
        
        google_response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_KEY}&q={search_query}&tbm=isch", headers=headers)
        google_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error getting search results: {e}")

    search_results = google_response.json()["items"]
    hasils = []
    for i in search_results:
        hasil = {
            'title' : i['title'],
            'link' : i['link'],
            'snippet': i['snippet']
        }
        hasils.append(hasil)
    return {'search_results': hasils}

# kelas menyimpan notes
class NotesMealPlan(BaseModel):
    id: int
    date: str
    title: str
    serving: Optional[int]=None
    time_prep: Optional[int]=None
    source: Optional[str]=None

data_meal = []

# generate meal plan random 
@app.get('/meal-plan')
async def meal_plan():
    url = f"https://api.spoonacular.com/mealplanner/generate?apiKey={API_KEY}" 
    query_params = {'timeFrame': 'day'}
    
    response = requests.get(url, params=query_params) 
    data = response.json()
    print(data)
    return data

# melakukan generate random pada rencana makanan dalam sehari dan 
# mendaftarkannya pada daftar notes meal plan dengan tanggal random
@app.get('/meal-plan/add/')
async def meal_plan_add():
    data_get = await meal_plan()
    print(data_get)
    for each in data_get['meals']:
        note_meal = NotesMealPlan(
            id = each['id'],
            date = random_date(),
            title = each['title'],
            serving = each['servings'],
            time_prep = each['readyInMinutes'],
            source = each['sourceUrl']
        )
        data_meal.append(note_meal)
    return {'message': 'Meal plan created successfully.'}

# fungsi bantuan untuk randomize tanggal dalam tahun 2023
def random_date():
    # Generate a random date between two dates between 2023
    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    formatted_date = random_date.strftime('%d-%m-%Y')
    return formatted_date

# menambah manual plan meal 
@app.post('/notes-meal-plan/add/')
def add_meal_plan(note_meal:NotesMealPlan):
    data_meal.append(note_meal)
    return {'message': 'Meal plan created successfully.'}

# melihat notes meal plan yang sudah dibuat
@app.get('/notes-meal-plan/')
async def get_meal_plan():
    result = [
        {
        'id':data.id,
        'date':data.date,
        'title':data.title,
        'serving':data.serving,
        'time_prep':data.time_prep,
        'source':data.source
        }
        for data in data_meal]
    return {'results':result}