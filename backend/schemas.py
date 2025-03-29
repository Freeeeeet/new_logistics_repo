from pydantic import BaseModel, condecimal, field_validator, EmailStr
from datetime import datetime
from typing import Optional, Union


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


    @field_validator("start_date", "end_date")
    @classmethod
    def make_naive(cls, value):
        if value and value.tzinfo:
            return value.replace(tzinfo=None)
        return value


class OrderAssignmentCreate(BaseModel):
    order_id: int
    driver_id: int
    vehicle_id: int
    start_date: datetime
    end_date: datetime

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_datetime(cls, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "driver_id": 1,
                "vehicle_id": 1,
                "start_date": "2025-03-31 13:20",
                "end_date": "2025-04-01 18:45"
            }
        }


class OrderAssignmentUpdate(BaseModel):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrderAssignment(OrderAssignmentBase):
    id: int

    class Config:
        from_attributes = True

# --- Клиенты ---
class ClientBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True


# --- Грузы ---
class CargoBase(BaseModel):
    description: Optional[str] = None
    weight: condecimal(max_digits=10, decimal_places=2)
    volume: condecimal(max_digits=10, decimal_places=2)


class CargoCreate(CargoBase):
    pass


class Cargo(CargoBase):
    id: int

    class Config:
        from_attributes = True


# --- Маршруты ---
class RouteBase(BaseModel):
    origin: str
    destination: str
    distance: condecimal(max_digits=10, decimal_places=2)


class RouteCreate(RouteBase):
    pass


class Route(RouteBase):
    id: int

    class Config:
        from_attributes = True

# --- Заказы ---
class OrderBase(BaseModel):
    client_id: int
    cargo_id: int
    warehouse_id: Optional[int] = None
    route_id: int
    status_id: int = 1


class OrderCreateFull(BaseModel):
    client: Union[int, ClientCreate]
    cargo: CargoCreate
    route: Union[int, RouteCreate]
    warehouse_id: Optional[int] = None



