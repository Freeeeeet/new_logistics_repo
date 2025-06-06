from pydantic import BaseModel, condecimal, field_validator, EmailStr, Field
from datetime import datetime
from typing import Optional, Union
from decimal import Decimal

class OrderBase(BaseModel):
    client_id: int
    cargo_id: int
    warehouse_id: Optional[int] = None
    route_id: int
    status_id: int


class OrderCreate(OrderBase):
    pass

class OrderCreateNorm(BaseModel):
    client_name: str
    client_email: str
    client_phone: str
    cargo_description: str
    cargo_weight: int
    cargo_volume: int
    route_id: int
    warehouse_id: int

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    client_name: Optional[str]
    client_email: Optional[str]
    client_phone: Optional[str]
    cargo_description: Optional[str]
    cargo_weight: Optional[Decimal]
    cargo_volume: Optional[Decimal]
    route_id: Optional[int]
    warehouse_id: Optional[int]


class OrderWithDetails(BaseModel):
    order_id: int
    is_paid: Optional[int]
    client_name: str
    client_email: str
    order_status: str
    origin: str
    destination: str
    warehouse_name: Optional[str]
    warehouse_location: Optional[str]
    cargo_description: Optional[str]
    cargo_weight: Optional[Decimal]
    cargo_volume: Optional[Decimal]

    class Config:
        orm_mode = True

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
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientUpdate(ClientBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class Client(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True


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


# Модели маршрута
class RouteBase(BaseModel):
    origin: str
    destination: str
    distance: condecimal(max_digits=10, decimal_places=2)


# Модель для создания маршрута
class RouteCreate(BaseModel):
    origin: str
    destination: str
    distance: float

# Модель маршрута для возвращаемого ответа
class Route(BaseModel):
    id: int
    origin: str
    destination: str
    distance: Decimal

    class Config:
        orm_mode = True


# --- Заказы ---
class OrderBase(BaseModel):
    client_id: int
    cargo_id: int
    warehouse_id: Optional[int] = None
    route_id: int
    status_id: int


class OrderCreateFull(OrderBase):
    cargo: CargoCreate
    route: RouteCreate

# Схема для отображения складов
class WarehouseBase(BaseModel):
    name: str
    location: str

    class Config:
        orm_mode = True

# Схема для создания склада
class WarehouseCreate(WarehouseBase):
    pass

# Схема для обновления склада
class WarehouseUpdate(WarehouseBase):
    pass

# Схема для ответа по складам
class Warehouse(WarehouseBase):
    id: int

    class Config:
        orm_mode = True



class OrderFilter(BaseModel):
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    warehouse_name: Optional[str] = None
    warehouse_location: Optional[str] = None


class UserCreateRequest(BaseModel):
    username: str = Field(..., pattern=r'^[A-Za-z0-9_-]{3,20}$',
                          description="Must be 3-20 characters: letters, numbers, _ and - only.",
                          examples=["RyanGosling123"])
    email: EmailStr = Field(..., description="Must be valid e-mail address.", examples=["gosling@gmail.com"])
    full_name: str = Field(..., pattern=r'^[\w\sа-яА-ЯёЁ-]{1,50}$',
                           description="Must be 1-50 characters: letters (any language), numbers, spaces, and - only.",
                           examples=["Ryan Gosling"])
    password: str = Field(..., pattern=r'^.{8,50}$',
                          description="Password must be between 8 and 50 characters.", examples=["StrongPass123"])

    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    success: bool

    class Config:
        from_attributes = True


class LoginUserRequest(BaseModel):
    username: str = Field(..., pattern=r'^[A-Za-z0-9_-]{3,20}$',
                          description="Must be 3-20 characters: letters, numbers, _ and - only.",
                          examples=["RyanGosling123"])
    password: str = Field(..., pattern=r'^.{8,50}$',
                          description="Password must be between 8 and 50 characters.", examples=["StrongPass123"])

    class Config:
        from_attributes = True


class LoginUserResponse(BaseModel):
    token: str

