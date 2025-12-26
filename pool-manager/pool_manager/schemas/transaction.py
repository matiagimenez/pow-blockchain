import re
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, TypeAdapter, field_validator

ADDRESS_REGEX = re.compile(r"^0x[a-fA-F0-9]{40}$")


class Transaction(BaseModel):
    id_: UUID = Field(alias="id", default_factory=uuid4)
    sender: str
    receiver: str
    amount: float
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

    @field_validator("sender", "receiver")
    def validate_wallet_address(cls, address: str) -> str:
        if not ADDRESS_REGEX.match(address):
            raise ValueError(f"Invalid wallet address format: {address}")
        return address


Transactions = TypeAdapter(list[Transaction])
