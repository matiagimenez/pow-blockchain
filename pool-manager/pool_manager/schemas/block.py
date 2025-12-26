from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .transaction import Transaction, Transactions


class Block(BaseModel):
    previous_hash: str
    transactions: list[Transaction]
    index: int
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    hash_: str = Field(alias="hash", default="")
    nonce: int = Field(default=0)

    def to_dict(self) -> dict[str, Any]:
        data = self.model_dump(by_alias=True, mode="json", exclude={"transactions"})
        data["transactions"] = Transactions.dump_json(self.transactions)
        return data
