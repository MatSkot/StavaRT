from datetime import datetime

from pydantic import BaseModel, Field, ValidationError, validator, root_validator
from pydantic.types import List


class GeoCoords(BaseModel):

    latitude: float
    longitude: float

    @validator('latitude', 'longitude', pre=True)
    def string2float(cls, v):
        if v and isinstance(v, str):
            v = float(v.replace(',', '.').strip())
        return v

    @validator('latitude')
    def lat_validator(cls, v):
        if v is not None and abs(v) <= 90:
            return v
        raise ValidationError(f'Incorrect Latitude value: {v}')

    @validator('longitude')
    def lon_validator(cls, v):
        if v is not None and abs(v) <= 180:
            return v
        raise ValidationError(f'Incorrect Longitude value: {v}')


class GeoPath(BaseModel):

    geo_path: List[GeoCoords]

    @validator('geo_path', pre=True)
    def pat_converter(cls, values):
        for i, v in enumerate(values):
            lat, lon = v.split(':')
            values[i] = GeoCoords(
                latitude=lat,
                longitude=lon)
        return values

    @validator('geo_path')
    def geo_validator(cls, v):
        reason = ''
        if len(v) < 2:
            reason = 'short'
        elif len(v) > 50:
            reason = 'long'
        if reason:
            raise ValueError(
                f'Geo path is to {reason}, path length {len(v)}. \
                Minimum 2 geo points, Maximum 50 geo points')
        return v


class GeoDistance(BaseModel):

    distance: float


class ApiRequest(GeoPath):

    request_id: str
    geo_path: List[GeoCoords]


class ApiResponse(BaseModel):

    status: str = "ok"
    request: ApiRequest
    distances: List[float]
    start_time: datetime
    finish_time: datetime = Field(default_factory=datetime.utcnow)
    total_distance: float

    @property
    def execitoon_time(cls):
        return cls.finish_time - cls.start_time

    @property
    def max_distance(cls):
        return cls.finish_time - cls.start_time

    @property
    def min_distance(cls):
        return cls.finish_time - cls.start_time

    @property
    def avg_distance(cls):
        return cls.finish_time - cls.start_time


class ApiError(BaseModel):

    status: str = "error"
    code: int = 666
    message: str = ""


class RemoteRequest(BaseModel):
    method: str = "GET"
    url: str
    params: dict = {}
    headers: dict = {}
    timeout: int = 10

    response: bytes = None
