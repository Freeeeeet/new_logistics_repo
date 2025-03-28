from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class OrderStatusBase(BaseModel):
    name: str


class OrderStatusCreate(OrderStatusBase):
    pass


class OrderStatus(OrderStatusBase):
    id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True


class CargoBase(BaseModel):
    description: Optional[str] = None
    weight: float
    volume: float


class CargoCreate(CargoBase):
    pass


class Cargo(CargoBase):
    id: int

    class Config:
        orm_mode = True


class WarehouseBase(BaseModel):
    name: str
    location: str


class WarehouseCreate(WarehouseBase):
    pass


class Warehouse(WarehouseBase):
    id: int

    class Config:
        orm_mode = True


class RouteBase(BaseModel):
    origin: str
    destination: str
    distance: float


class RouteCreate(RouteBase):
    pass


class Route(RouteBase):
    id: int

    class Config:
        orm_mode = True


class VehicleBase(BaseModel):
    license_plate: str
    model: str


class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    id: int

    class Config:
        orm_mode = True


class DriverBase(BaseModel):
    name: str
    license_number: str


class DriverCreate(DriverBase):
    pass


class Driver(DriverBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    client_id: int
    cargo_id: int
    warehouse_id: Optional[int] = None
    route_id: int
    status_id: int
    created_at: Optional[datetime] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    client: Client
    cargo: Cargo
    warehouse: Optional[Warehouse]
    route: Route
    status: OrderStatus

    class Config:
        orm_mode = True


class OrderAssignmentBase(BaseModel):
    order_id: int
    driver_id: int
    vehicle_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrderAssignmentCreate(OrderAssignmentBase):
    pass


class OrderAssignment(OrderAssignmentBase):
    id: int
    driver: Driver
    vehicle: Vehicle

    class Config:
        orm_mode = True


class CargoMovementBase(BaseModel):
    cargo_id: int
    warehouse_id: int
    movement_date: Optional[datetime] = None


class CargoMovementCreate(CargoMovementBase):
    pass


class CargoMovement(CargoMovementBase):
    id: int

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_date: Optional[datetime] = None


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True