from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes import base_router

app = FastAPI()  # type: ignore[arg-type]

app.include_router(base_router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
