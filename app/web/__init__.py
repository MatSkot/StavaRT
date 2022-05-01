from fastapi import APIRouter

router = APIRouter()


@router.get('/', tags=['WEB'])
async def index():
    return


@router.get('/distance', tags=['WEB'])
async def distance():
    return
