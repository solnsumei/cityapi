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
        return ""

    @classmethod
    async def get_current_time(cls, obj, session):
        async with session.get(f"{world_api_url}/{obj.timezone}") as response:
            result = await response.json()
            current_time = "No data" if "error" in result else result["datetime"]
            obj.current_time = current_time

    class PydanticMeta:
        computed = ('current_time',)


City_Pydantic = pydantic_model_creator(City, name="City")
CityIn_Pydantic = pydantic_model_creator(City, name="CityIn", exclude_readonly=True)
