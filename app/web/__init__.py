from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

static = StaticFiles(directory="app/web/static")
templates = Jinja2Templates(directory="app/web/templates")


@router.get('/', response_class=HTMLResponse, tags=['WEB'])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get('/distance', response_class=HTMLResponse, tags=['WEB'])
async def distance():
    return
