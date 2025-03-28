from pydantic import BaseModel
from typing import Optional


# Модель для создания заказа
class OrderCreate(BaseModel):
    client_id: int
    cargo_id: int
    status: str
    price: float
    quantity: int
    # Добавь другие поля, если необходимо


# Модель для обновления заказа
class OrderUpdate(BaseModel):
    client_id: Optional[int] = None
    cargo_id: Optional[int] = None
    status: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    # Добавь другие поля, которые можно обновлять
