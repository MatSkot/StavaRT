import asyncio
import ujson

from app.libs.db import save_stats
from app.libs.tools import get_remote, basic_auth, utc_now
from app.libs.models import ApiRequest, ApiResponse, GeoCoords, RemoteRequest

from fastapi import APIRouter
from pydantic.types import List

router = APIRouter()

USERNAME = 'Cristoforo'
PASSWORD = 'Colombo'


async def geo_distance(origin: GeoCoords, dest: GeoCoords) -> float:
    data = await get_remote(
        RemoteRequest(
            method='GET',
            url='http://146.59.46.40:60080/route',
            params={
                'origin': f'{origin.latitude},{origin.longitude}',
                'destination': f'{dest.latitude},{dest.longitude}'
            },
            headers={'Authorization': basic_auth(USERNAME, PASSWORD)}
        )
    )
    try:
        j = ujson.loads(data.response)
        return j['distance']
    except Exception as e:
        print(data.response)
        print("Failed to parse geo distance: ", e)
    return 0.0


async def get_distance_for_path(path: List[GeoCoords]) -> List[float]:
    iterations = len(path)-1
    tasks = [geo_distance(g, path[i+1]) for i, g in enumerate(path) if i < iterations]
    return await asyncio.gather(*tasks)


@router.post('/api/calc_distance', response_model=ApiResponse, tags=['API'])
async def distance_api(request: ApiRequest):
    """
    Calculates distance between two geo points.
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
        await save_stats(response.total_distance, response.start_time, response.finish_time)
    except Exception as e:
        print("Failed to save statistics: ", e)

    return response
