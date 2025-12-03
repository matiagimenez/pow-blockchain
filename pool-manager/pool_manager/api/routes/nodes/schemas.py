from pydantic import BaseModel, Field


class NodeKeepAliveRequest(BaseModel):
    node_id: str = Field(description="Unique identifier of the node sending the signal")
    ip_address: str = Field(description="IP address of the node sending the  signal")
    timestamp: int = Field(description="Timestamp when the keep-alive signal was sent")
    miner_type: str = Field(..., description="Type of miner - CPU or GPU")
