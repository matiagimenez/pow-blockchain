from typing import Any

from pydantic import BaseModel, Field

from pow_miner.utils import Settings


class Task(BaseModel):
    challenge: str = Field(default_factory=lambda: Settings.HASH_CHALLENGE)
    data: dict[str, Any]


class TaskResult(BaseModel):
    nonce: int | None = Field(default=None)
    hash_: str | None = Field(alias="hash", default=None)
