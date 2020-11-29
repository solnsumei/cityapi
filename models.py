import requests
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

world_api_url = "http://worldtimeapi.org/api/timezone"


class City(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    timezone = fields.CharField(50)

    def current_time(self) -> str:
        r = requests.get(f"{world_api_url}/{self.timezone}")
        current_time = 'No data' if "error" in r.json() else r.json()["datetime"]
        return current_time

    class PydanticMeta:
        computed = ('current_time',)



City_Pydantic = pydantic_model_creator(City, name="City")
CityIn_Pydantic = pydantic_model_creator(City, name="CityIn", exclude_readonly=True)
