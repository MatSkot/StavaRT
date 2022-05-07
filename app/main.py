from fastapi import FastAPI

import app.geodistance as geodistance
import app.web as web

from app.libs.db import stats_db, create_table

app = FastAPI(
    title="Stava recruitment task",
    description="",
    version="1.0.0",
)

app.include_router(geodistance.router)
app.include_router(web.router)

app.mount("/static", web.static, name="static")

@app.on_event("startup")
async def startup_event():
    await stats_db.connect()
    await create_table()


@app.on_event("shutdown")
async def shutdown_event():
    await stats_db.disconnect()
