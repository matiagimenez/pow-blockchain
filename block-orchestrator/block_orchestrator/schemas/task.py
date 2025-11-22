from typing import Any

from block_orchestrator.utils import Settings
from pydantic import BaseModel, Field


class Task(BaseModel):
    challenge: str = Field(default_factory=lambda: Settings.HASH_CHALLENGE)
    data: dict[str, Any]
