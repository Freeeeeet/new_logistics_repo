from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import Order, OrderCreate, OrderUpdate
from crud.orders_crud import get_all_orders, get_order_by_id, create_order, update_order, delete_order
from typing import List

router = APIRouter()


@router.get("/orders", response_model=List[Order])
async def read_orders(db: AsyncSession = Depends(get_db)):
    return await get_all_orders(db)


@router.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order_by_id(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders", response_model=Order)
async def create_new_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await create_order(db, order)


@router.put("/orders/{order_id}", response_model=Order)
async def update_existing_order(order_id: int, order_update: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await update_order(db, order_id, order_update)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/orders/{order_id}")
async def delete_existing_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await delete_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}