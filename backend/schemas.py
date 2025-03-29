from pydantic import BaseModel, condecimal
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


class CargoBase(BaseModel):
    description: Optional[str] = None
    weight: condecimal(max_digits=10, decimal_places=2)
    volume: condecimal(max_digits=10, decimal_places=2)


class CargoCreate(CargoBase):
    pass


class CargoUpdate(CargoBase):
    pass


class Cargo(CargoBase):
    id: int

    class Config:
        from_attributes = True

class OrderAssignmentBase(BaseModel):
    order_id: int
    driver_id: int
    vehicle_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrderAssignmentCreate(OrderAssignmentBase):
    pass


class OrderAssignmentUpdate(BaseModel):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrderAssignment(OrderAssignmentBase):
    id: int

    class Config:
        from_attributes = True