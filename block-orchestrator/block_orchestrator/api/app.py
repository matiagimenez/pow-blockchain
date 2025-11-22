from contextlib import asynccontextmanager

from block_orchestrator.helpers import process_transactions_and_build_block
from block_orchestrator.utils import Scheduler, Settings
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes import base_router, blocks_router, transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Scheduler.add_cronjob(
        job=process_transactions_and_build_block,
        interval=Settings.BLOCK_CREATION_INTERVAL,
    )
    Scheduler.start()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(transactions_router)
app.include_router(blocks_router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
