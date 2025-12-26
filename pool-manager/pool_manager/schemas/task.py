from typing import Any

from pydantic import BaseModel


class MiningTask(BaseModel):
    data: dict[str, Any]
    challenge: str
