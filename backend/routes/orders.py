from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Order
from database import get_db
from pydantic import BaseModel
from schemas import OrderCreate, OrderUpdate  # Убедись, что импортируешь нужные модели

router = APIRouter()


# Получение всех заказов
@router.get("/")
async def get_orders(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Order))
        orders = result.scalars().all()
    return orders


# Создание нового заказа
@router.post("/")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = Order(**order.dict())
    db.add(new_order)
    await db.commit()
    return new_order


# Получение одного заказа по ID
@router.get("/{order_id}")
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Обновление заказа
@router.put("/{order_id}")
async def update_order(order_id: int, order: OrderUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalar_one_or_none()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # Обновляем поля заказа
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)

    await db.commit()
    return db_order


# Удаление заказа
@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.delete(order)
    await db.commit()
    return {"message": "Order deleted successfully"}
