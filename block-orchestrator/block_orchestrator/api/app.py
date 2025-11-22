from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes import base_router, blocks_router, transactions_router

app = FastAPI()


app.include_router(base_router)
app.include_router(transactions_router)
app.include_router(blocks_router)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
