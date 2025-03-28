from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from models import Order, Client, Cargo, Route, OrderStatus, OrderAssignment, Payment, Warehouse
from database import get_db
from datetime import datetime

router = APIRouter()


# Получить все заказы
@router.get("/orders", response_model=list[Order])
async def get_all_orders(db: Session = Depends(get_db)):
    result = await db.execute(select(Order).all())
    orders = result.scalars().all()
    return orders


# Получить заказ по ID
@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    try:
        result = await db.execute(select(Order).filter(Order.id == order_id))
        order = result.scalars().one()
        return order
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


# Создать новый заказ
@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(
        client_id: int,
        cargo_id: int,
        warehouse_id: int,
        route_id: int,
        status_id: int,
        db: Session = Depends(get_db)
):
    new_order = Order(
        client_id=client_id,
        cargo_id=cargo_id,
        warehouse_id=warehouse_id,
        route_id=route_id,
        status_id=status_id,
        created_at=datetime.now()
    )
    db.add(new_order)
    await db.commit()
    return new_order


# Обновить статус заказа
@router.put("/orders/{order_id}", response_model=Order)
async def update_order_status(
        order_id: int,
        status_id: int,
        db: Session = Depends(get_db)
):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    order.status_id = status_id
    await db.commit()
    await db.refresh(order)
    return order


# Удалить заказ по ID
@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    await db.delete(order)
    await db.commit()


# Получить все заказы клиента по ID
@router.get("/clients/{client_id}/orders", response_model=list[Order])
async def get_orders_by_client(client_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(Order).filter(Order.client_id == client_id))
    orders = result.scalars().all()
    return orders


# Получить назначения водителя для конкретного заказа
@router.get("/orders/{order_id}/assignments", response_model=list[OrderAssignment])
async def get_order_assignments(order_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(OrderAssignment).filter(OrderAssignment.order_id == order_id))
    assignments = result.scalars().all()
    return assignments


# Получить все платежи для конкретного заказа
@router.get("/orders/{order_id}/payments", response_model=list[Payment])
async def get_order_payments(order_id: int, db: Session = Depends(get_db)):
    result = await db.execute(select(Payment).filter(Payment.order_id == order_id))
    payments = result.scalars().all()
    return payments