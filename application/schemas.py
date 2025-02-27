from pydantic import BaseModel
from typing import List


class CountrySchema(BaseModel):
    country_id: str
    probability: float


class UserSchema(BaseModel):
    name: str
    country: List[CountrySchema] = []


class UserSchemaResponse(BaseModel):
    counter: int
    name: str
    country: List[CountrySchema] = []

