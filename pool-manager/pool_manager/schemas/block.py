from datetime import datetime
from hashlib import md5
from typing import Any

from block_orchestrator.utils import Settings
from pydantic import BaseModel, Field

from .transaction import Transaction, Transactions


class Block(BaseModel):
    previous_hash: str
    transactions: list[Transaction]
    index: int
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    hash_: str = Field(alias="hash", default="")
    nonce: int = Field(default=0)

    @property
    def payload(self) -> str:
        return "".join(tx.content for tx in self.transactions)

    @property
    def content(self) -> str:
        return f"{self.index}{self.timestamp}{self.payload}{self.previous_hash}"

    def to_dict(self) -> dict[str, Any]:
        data = self.model_dump(by_alias=True, mode="json", exclude={"transactions"})
        data["transactions"] = Transactions.dump_json(self.transactions)
        return data

    # Calculates and validates the block hash - md5(nonce + md5(index+timestamp+data+previous_hash))
    @property
    def is_valid(self) -> bool:
        hash_challenge = Settings.HASH_CHALLENGE
        if hash_challenge and (not self.hash_.startswith(hash_challenge)):
            return False

        block_content_hash = md5(self.content.encode("utf-8")).hexdigest()
        md5_input = f"{int(self.nonce)}{block_content_hash}"
        calculated_hash = md5(md5_input.encode("utf-8")).hexdigest()

        return calculated_hash == self.hash_
