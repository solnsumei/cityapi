import aiohttp
import asyncio
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from models import City, City_Pydantic, CityIn_Pydantic


app = FastAPI()
session = None


@app.on_event("startup")
async def startup_event():
    global session
    session = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown():
    if session is not None:
        await session.close()


@app.get("/")
def index():
    return {"message": "Welcome to CityAPI"}


@app.get("/cities")
async def get_cities():
    cities = await City_Pydantic.from_queryset(City.all())
    global session

    tasks = []
    for city in cities:
        task = asyncio.create_task(City.get_current_time(city, session))
        tasks.append(task)

    await asyncio.gather(*tasks)
    return cities


@app.get("/cities/{city_id}")
async def get_city(city_id: int):
    city = await City_Pydantic.from_queryset_single(City.get(id=city_id))
    global session
    await City.get_current_time(city, session)
    return city


@app.post("/cities")
async def create_city(city: CityIn_Pydantic):
    city_obj = await City.create(**city.dict())
    return await City_Pydantic.from_tortoise_orm(city_obj)


@app.delete("/cities/{city_id}")
async def delete_city(city_id: int):
    await City.filter(id=city_id).delete()
    return {"message": "Delete successful"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
