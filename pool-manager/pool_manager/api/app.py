from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from pool_manager.services.pool_service import PoolService
from pool_manager.utils import Scheduler, Settings
from .routes import base_router, nodes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool_service = PoolService()
    await pool_service.start()

    Scheduler.add_cronjob(pool_service.check_pool_status, Settings.CHECK_POOL_STATUS_INTERVAL)
    Scheduler.start()

    yield

    await pool_service.stop()


app = FastAPI(lifespan=lifespan)  # type: ignore[arg-type]

app.include_router(base_router)
app.include_router(nodes_router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
