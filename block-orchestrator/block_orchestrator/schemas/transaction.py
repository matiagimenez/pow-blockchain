from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, TypeAdapter


class Transaction(BaseModel):
    id_: UUID = Field(alias="id", default_factory=uuid4)
    sender: str
    receiver: str
    amount: float
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))

    @property
    def content(self) -> str:
        return "".join(self.model_dump_json(by_alias=True))


Transactions = TypeAdapter(list[Transaction])
