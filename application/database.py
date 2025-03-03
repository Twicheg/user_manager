import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from application.models import Base
from dotenv import load_dotenv

load_dotenv(".env")

sql_filename = os.getenv("DB_NAME")
engine = create_engine(f"sqlite:///{sql_filename}", echo=True)


def create_tables() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
