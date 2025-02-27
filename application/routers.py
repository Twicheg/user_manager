from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.database import SessionDep
from application.models import Users, Countries
from application.schemas import UserSchema, UserSchemaResponse

names_router = APIRouter(prefix="/names")


@names_router.get("/", response_model=List[UserSchemaResponse])
async def get_users(session: SessionDep, name: str = ''):
    if name:
        return session.query(Users).filter(Users.name == name)
    return session.query(Users).all()


@names_router.post('/', status_code=201, response_model=UserSchemaResponse)
async def create_user(user: UserSchema, session: Depends(SessionDep)):
    user = Users(name=user.name, country=[Countries(**i.dict()) for i in user.country])
    session.add(user)
    session.commit()
    return user
