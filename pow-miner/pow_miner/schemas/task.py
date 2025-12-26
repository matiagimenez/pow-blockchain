from typing import Any

from pydantic import BaseModel, Field


class Task(BaseModel):
    challenge: str
    data: dict[str, Any]
    start_nonce: int
    end_nonce: int


class TaskResult(BaseModel):
    nonce: int | None = Field(default=None)
    hash_: str | None = Field(alias="hash", default=None)
