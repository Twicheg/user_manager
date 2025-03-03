import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from application.redis_conf import connect_to_redis, close_redis
from application.routers import names_router

app = FastAPI(docs_url="/documentation", redoc_url=None)


@app.on_event('startup')
async def startup_event():
    if os.getenv("redis") == "ON":
        await connect_to_redis()


@app.on_event('shutdown')
async def shutdown_event():
    if os.getenv("redis") == "ON":
        await close_redis()

app.include_router(names_router)

app.mount("/static", StaticFiles(directory="static"), name='static')

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, tags=["web"])
async def main(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

