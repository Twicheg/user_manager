from fastapi import FastAPI, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select

from application.database import create_tables, get_session, SessionDep
from application.models import Users

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


app.mount("/static", StaticFiles(directory="static"), name='static')
router = APIRouter(prefix="/names")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, session: SessionDep):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )


@router.get("/")
async def get_users(session: SessionDep, name: str = ''):
    pass


@router.post('/')
async def create_user(session: SessionDep):
    pass


app.include_router(router)
