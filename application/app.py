from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from application.database import create_tables, SessionDep
from application.routers import names_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_tables()


app.mount("/static", StaticFiles(directory="static"), name='static')
app.include_router(names_router)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, tags=["web"])
async def main(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )
