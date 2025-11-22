from typing import Any

from pydantic import BaseModel, Field

from block_orchestrator.utils import Settings


class Task(BaseModel):
    challenge: str = Field(default_factory=lambda: Settings.HASH_CHALLENGE)
    data: dict[str, Any]
