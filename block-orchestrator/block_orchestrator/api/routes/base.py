from fastapi import APIRouter

base_router = APIRouter(tags=["Healthcheck"])


@base_router.get("/healthcheck")
def healthcheck():
    return {"status": "200", "description": "Block orchestrator is running"}
