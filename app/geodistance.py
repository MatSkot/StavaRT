import asyncio
import functools
import logging
import orjson
import traceback

from pydantic import ValidationError

from app.libs.db import save_stats
from app.libs.tools import get_remote, basic_auth, utc_now, do_lprofile
from app.libs.models import ApiRequest, ApiResponse, GeoCoords, RemoteRequest, ApiError

from fastapi import APIRouter
from pydantic.types import List

from app.settings import GEODISTANCE_USERNAME, GEODISTANCE_PASSWORD

router = APIRouter()

logger = logging.getLogger()


def ensure_generic_response(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            logger.error(f'invalid request: {e}')
            return ApiError(message='invalid request')
        except Exception as e:
            logger.error(f'Unexcepted error occures :{e}\n{traceback.format_exc()}')
            return ApiError(message='Unexcepted error occures')
    return wrapped


async def geo_distance(origin: GeoCoords, dest: GeoCoords) -> float:
    data = await get_remote(
        RemoteRequest(
            method='GET',
            url='http://146.59.46.40:60080/route',
            params={
                'origin': f'{origin.latitude},{origin.longitude}',
                'destination': f'{dest.latitude},{dest.longitude}'
            },
            headers={'Authorization': basic_auth(GEODISTANCE_USERNAME, GEODISTANCE_PASSWORD)}
        )
    )
    try:
        j = orjson.loads(data.response)
        return j['distance']
    except Exception as e:
        logger.error(f"Failed to parse geo distance: {e}\n{data.response}")
    return 0.0


async def get_distance_for_path(path: List[GeoCoords]) -> List[float]:
    iterations = len(path)-1
    tasks = [geo_distance(g, path[i+1]) for i, g in enumerate(path) if i < iterations]
    return await asyncio.gather(*tasks)


@router.post('/api/calc_distance', response_model=ApiResponse, tags=['API'])
@ensure_generic_response
async def distance_api(request: ApiRequest):
    """
    Calculates distance between two geo points. Path must be between 2 and 50 geo points.
    Each point should contain valid latitude and longitude. Returns start and finish times,
    partial distance between consecutive points and total distance between all points.
    """
    start_time = utc_now()

    results = await get_distance_for_path(request.geo_path)

    response = ApiResponse(
        request=request,
        distances=results,
        start_time=start_time,
        total_distance=sum(results)
    )
    try:
        await save_stats(request.request_id, response.start_time, response.finish_time)
    except Exception as e:
        logger.error(f"Failed to save statistics: {e}")

    return response
