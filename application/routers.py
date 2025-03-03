from typing import List, Annotated

from fastapi import APIRouter, Query, HTTPException

from application.database import SessionDep
from application.models import Users
from application.schemas import UserSchema, UserSchemaResponse
from application.service import get_user_from_request, add_to_database
from application.redis_conf import get_redis, set_redis

tags_metadata = [
    {
        "name": "user",
        "description": "Operations with users. The **login** logic is also here.",
    }, ]

names_router = APIRouter(prefix="/names", tags=tags_metadata)


@names_router.get("/",
                  status_code=200,
                  tags=['user'],
                  response_model=List[UserSchemaResponse])
async def get_users(session: SessionDep,
                    name: Annotated[str | None, Query(max_length=20)] = None,
                    ):
    if name:
        cache = await get_redis(name)
        if cache is not None:
            return cache
        user_query = session.query(Users).filter(Users.name == name)
        users_with_that_name = [user for user in user_query]
        if users_with_that_name:
            await set_redis(user_query[0])
            return user_query
        else:
            user = await get_user_from_request(name)
            if user:
                user = await add_to_database(user, session)
                await set_redis(user)
                return [user]
            else:
                raise HTTPException(status_code=404, detail="Not found")

    return session.query(Users).all()


@names_router.post('/',
                   status_code=201,
                   tags=['user'],
                   response_model=UserSchemaResponse)
async def create_user(user: UserSchema, session: SessionDep):
    user = await add_to_database(user, session)
    return user
