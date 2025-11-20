from datetime import datetime
from hashlib import md5
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from block_orchestrator.utils import Settings


class Transaction(BaseModel):
    id_: UUID = Field(alias="id", default_factory=uuid4)
    sender: str
    receiver: str
    amount: float
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

    @property
    def content(self) -> str:
        return "".join(self.model_dump_json(by_alias=True))

    


class Block(BaseModel):
    timestamp: str
    hash_: str = Field(alias="hash")
    previous_hash: str
    transactions: list[Transaction]
    index: int
    nonce: int

    @property
    def payload(self) -> str:
        return "".join(tx.content for tx in self.transactions)

    @property
    def content(self) -> str:
        return f"{self.index}{self.timestamp}{self.payload}{self.previous_hash}"

    # Calculates and validates the block hash - md5(nonce + md5(index+timestamp+data+previous_hash))
    def is_valid(self) -> bool:
        hash_challenge = Settings.HASH_CHALLENGE
        if hash_challenge and (not self.hash_.startswith(hash_challenge)):
            return False

        block_content_hash = md5(self.content.encode("utf-8")).hexdigest()
        md5_input = f"{int(self.nonce)}{block_content_hash}"
        calculated_hash = md5(md5_input.encode("utf-8")).hexdigest()

        return calculated_hash == self.hash_
