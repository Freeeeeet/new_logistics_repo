from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    client_id: int
    cargo_id: int

class OrderResponse(BaseModel):
    id: int
    client_id: int
    cargo_id: int
    created_at: datetime

    class Config:
        from_attributes = True