import functools
import traceback

from typing import List, Optional

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import ValidationError

from app.geodistance import get_distance_for_path
from app.libs.models import GeoPath

router = APIRouter()

static = StaticFiles(directory="static")
templates = Jinja2Templates(directory="templates")


def error_page(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            print(e)
            return templates.TemplateResponse("error.html", {
                "request": kwargs['request'],
                "error": 'invalid request'})
        except Exception:
            print(traceback.format_exc())
            return templates.TemplateResponse("error.html", {
                "request": kwargs['request'],
                "error": 'unexcepted error'})
    return wrapped


@router.get('/', response_class=HTMLResponse, tags=['WEB'])
@error_page
async def index(
        request: Request,
        p: Optional[List[str]] = Query(
            None,
            regex=r'^([0-9]{1,3}\.?[0-9]*)\:([0-9]{1,3}\.?[0-9]*)$')):
    distance = ''
    if p is not None:
        path = GeoPath(geo_path=p)
        results = await get_distance_for_path(path.geo_path)
        distance = sum(results)
    return templates.TemplateResponse("index.html", {"request": request, "distance": distance})
