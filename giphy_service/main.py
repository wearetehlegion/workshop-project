import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
GIPHY_SEARCH_URL = "https://api.giphy.com/v1/gifs/search"

class TextRequest(BaseModel):
    text: str

class GifResponse(BaseModel):
    gif_url: str

def extract_keywords(text: str) -> str:
    """
    Примитивная эвристика: переводим на английский через словарь.
    Для MVP: можно расширить через интеграцию с переводчиком.
    """
    # Простейший словарь для демонстрации
    keywords_dict = {
        "космос": "space",
        "приключения": "adventure",
        "кот": "cat",
        "собака": "dog",
        "любовь": "love",
        "танец": "dance",
        "музыка": "music",
        "машина": "car",
        "работа": "work",
        "отдых": "relax",
        "еда": "food",
        "праздник": "holiday",
        "деньги": "money",
        "спорт": "sport",
        "игра": "game",
        "путешествие": "travel",
        "дружба": "friendship",
        "радость": "joy",
        "грусть": "sad",
        "страх": "fear",
        "счастье": "happiness",
        "история": "story",
        "комедия": "comedy",
        "драма": "drama",
        "фильм": "movie",
        "приключение": "adventure",
        "космический": "space",
        "приключениях": "adventure",
        "космических": "space",
    }
    # Ищем ключевые слова
    text_lower = text.lower()
    found = []
    for ru, en in keywords_dict.items():
        if ru in text_lower and en not in found:
            found.append(en)
    # Если ничего не найдено — fallback
    if not found:
        return "funny"
    # Возвращаем 1-2 ключевых слова
    return " ".join(found[:2])

@app.post("/gif", response_model=GifResponse)
def get_gif(req: TextRequest):
    keywords = extract_keywords(req.text)
    params = {
        "api_key": GIPHY_API_KEY,
        "q": keywords,
        "limit": 1,
        "rating": "pg"
    }
    response = requests.get(GIPHY_SEARCH_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Giphy API error")
    data = response.json()
    if not data.get("data"):
        raise HTTPException(status_code=404, detail="No GIF found")
    gif_url = data["data"][0]["images"]["original"]["url"]
    return GifResponse(gif_url=gif_url)