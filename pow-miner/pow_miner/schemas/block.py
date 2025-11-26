from datetime import datetime

from pydantic import BaseModel, Field, field_validator

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

    @field_validator("transactions", mode="before")
    def validate_transactions(
        transactions: list[Transaction],
    ) -> list[Transaction]:
        return Transactions.validate_json(transactions)
