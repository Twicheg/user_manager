from typing import List, Annotated

from fastapi import APIRouter, Query, HTTPException
from application.database import SessionDep
from application.models import Users
from application.schemas import UserSchema, UserSchemaResponse
from application.service import get_user_from_request, add_to_database

names_router = APIRouter(prefix="/names")


@names_router.get("/",
                  status_code=200,
                  tags=['user'],
                  response_model=List[UserSchemaResponse])
async def get_users(session: SessionDep,
                    name: Annotated[str | None, Query(max_length=20)] = None,
                    url: str | None = None):
    if name:
        user_query = session.query(Users).filter(Users.name == name)
        users_with_that_name = [user for user in user_query]
        if users_with_that_name:
            return user_query

        else:
            user = await get_user_from_request(name, url)
            if user:
                user = await add_to_database(user, session)
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
