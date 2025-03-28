from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderBase(BaseModel):
    client_id: int
    cargo_id: int
    warehouse_id: Optional[int] = None
    route_id: int
    status_id: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True