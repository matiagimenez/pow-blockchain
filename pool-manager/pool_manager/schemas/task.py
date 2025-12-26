from pydantic import BaseModel

from .block import Block


class MiningTask(BaseModel):
    block: Block
    challenge: str
