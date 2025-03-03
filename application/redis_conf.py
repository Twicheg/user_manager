import os
import pickle
from typing import List

import redis

from application.models import Users
from application.schemas import CountrySchema, UserForRedisSchema

connect = None


async def connect_to_redis() -> None:
    global connect
    connect = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")))


async def close_redis() -> None:
    if connect:
        connect.close()
        await connect.wait_closed()


async def get_redis(name: str) -> List|None:
    try:
        cache = connect.get(name)
    except Exception:
        return None
    if cache is not None:
        response = pickle.loads(cache)
        return [{"name": response.name, "counter": response.counter, "country": [i.dict() for i in response.country]}]

    return None


async def set_redis(user: Users) -> None:
    name = user.name
    user = UserForRedisSchema(name=user.name, counter=user.counter,
                              country=[CountrySchema(country_id=i.country_id, probability=i.probability) for i in
                                       user.country])
    p_mydict = pickle.dumps(user)
    try:
        connect.set(name, p_mydict, ex=600)
    except Exception:
        return None