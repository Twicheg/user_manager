from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from typing import List

from application.models import Users

from application.database import get_session


class CountrySchema(BaseModel):
    country_id: str
    probability: float

    @field_validator('country_id', mode="before")
    @classmethod
    def check(cls, country_id: str) -> str:
        if len(country_id) > 5:
            raise HTTPException(status_code=422,
                                detail="max size of country_id is 5")
        return country_id


class UserSchema(BaseModel):
    name: str
    country: List[CountrySchema]

    @field_validator('name', mode="before")
    @classmethod
    def check(cls, name: str) -> str:
        if not name or name in [i.name for i in get_session().__next__().query(Users).all()]:
            raise HTTPException(status_code=422, detail="User must be unique")
        return name


class UserSchemaResponse(BaseModel):
    counter: int
    name: str
    country: List[CountrySchema]


class UserForRedisSchema(BaseModel):
    name: str
    counter: int
    country: List[CountrySchema] = []
