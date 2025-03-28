from pydantic import BaseModel
from typing import Optional


class OrderBase(BaseModel):
    client_id: int
    cargo_id: int
    quantity: int
    price: float


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    client_id: Optional[int] = None
    cargo_id: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
