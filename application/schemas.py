from pydantic import BaseModel
from typing import List, Dict


class Country(BaseModel):
    country_id: str
    probability: float


class User(BaseModel):
    count: int
    name: str
    country: List[Dict[Country]]
