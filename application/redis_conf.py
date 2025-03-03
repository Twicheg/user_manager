import os
import logging
import pickle
from typing import List

import redis

from application.models import Users
from application.schemas import CountrySchema, UserForRedisSchema

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)


async def connect_to_redis() -> redis:
    connect = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")))
    return connect


async def get_redis() -> redis:
    try:
        r = await connect_to_redis()
        return r
    finally:
        r.close()


async def check_in_redis(name: str) -> List:
    cache = await get_redis()
    cache = cache.get(name)
    if cache is not None:
        response = pickle.loads(cache)
        return [{"name": response.name, "counter": response.counter, "country": [i.dict() for i in response.country]}]

    return None


async def set_redis(user: Users) -> None:
    cache = await get_redis()
    name = user.name
    user = UserForRedisSchema(name=user.name, counter=user.counter,
                              country=[CountrySchema(country_id=i.country_id, probability=i.probability) for i in
                                       user.country])
    p_mydict = pickle.dumps(user)
    cache.set(name, p_mydict, ex=600)
