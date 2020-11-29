from fastapi import FastAPI
from pydantic import BaseModel
import requests


app = FastAPI()

db = []
world_api_url = "http://worldtimeapi.org/api/timezone"


class City(BaseModel):
    name: str
    timezone: str


def fetch_current_time_for_city(city: dict[str: str]):
    r = requests.get(f"{world_api_url}/{city['timezone']}")
    current_time = None if "error" in r.json() else r.json()["datetime"]
    return {"name": city["name"], "timezone": city["timezone"], "current_time": current_time}


@app.get("/")
def index():
    return {"message": "Welcome to CityAPI"}


@app.get("/cities")
async def get_cities():
    results = []
    for city in db:
        city_with_current_time = fetch_current_time_for_city(city)
        results.append(city_with_current_time)
    return results


@app.get("/cities/{city_id}")
async def get_city(city_id: int):
    return fetch_current_time_for_city(db[city_id-1])


@app.post("/cities")
async def create_city(city: City):
    db.append(city.dict())
    return db[-1]


@app.delete("/cities/{city_id}")
async def delete_city(city_id: int):
    db.pop(city_id-1)
    return {"message": "Delete successful"}
