import asyncio
import json

from app.libs.tools import get_remote, basic_auth, utc_now
from app.libs.models import ApiRequest, ApiResponse, GeoCoords, RemoteRequest

from fastapi import APIRouter

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
        j = json.loads(data.response)
        return j['distance']
    except Exception as e:
        print("Failed to parse geo distance: ", e)
    return 0


@router.post('/api/calc_distance', response_model=ApiResponse, tags=['API'])
async def distance_api(request: ApiRequest):
    """
    Calculates distance between two.
    """
    start_time = utc_now()
    path = request.geo_path
    iterations = len(path)-1
    tasks = [geo_distance(g, path[i+1]) for i, g in enumerate(path) if i < iterations]

    results = await asyncio.gather(*tasks)

    return ApiResponse(
        request=request,
        distances=results,
        start_time=start_time,
        total_distance=sum(results)
    )
