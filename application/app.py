
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from application.database import create_tables, get_session, SessionDep
from application.models import Users, Countries
from application.routers import names_router
from application.schemas import UserSchema, UserSchemaResponse

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


app.mount("/static", StaticFiles(directory="static"), name='static')
app.include_router(names_router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )


