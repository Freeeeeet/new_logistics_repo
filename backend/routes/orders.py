from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import Order, OrderCreate, OrderUpdate, OrderCreateNorm, OrderWithDetails, OrderFilter

from crud.orders_crud import (get_all_orders, get_order_by_id, create_order, update_order, delete_order, create_order_full,
                              update_order_full, get_filtered_orders)
from typing import List
from utils.user_auth import check_user_auth_final
from crud.users_crud import check_auth
router = APIRouter()


@router.get("/", response_model=List[OrderWithDetails])
async def read_orders(db: AsyncSession = Depends(get_db), authorization: str = Header(None),):
    user_id = await check_user_auth_final(db, authorization)
    return await get_all_orders(db)


@router.get("/{order_id}", response_model=Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db), authorization: str = Header(None),):
    user_id = await check_user_auth_final(db, authorization)
    order = await get_order_by_id(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/filter/", response_model=List[OrderWithDetails])  # Изменили метод на GET
async def filter_orders(
    client_name: str = None,  # Пример параметров, которые можно передавать как query parameters
    client_email: str = None,
    warehouse_name: str = None,
    warehouse_location: str = None,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    user_id = await check_user_auth_final(db, authorization)
    filters = OrderFilter(
        client_name=client_name,
        client_email=client_email,
        warehouse_name=warehouse_name,
        warehouse_location=warehouse_location
    )
    return await get_filtered_orders(db, filters, user_id)

@router.post("/create", response_model=Order)
async def create_new_order(order: OrderCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(None),):
    user_id = await check_user_auth_final(db, authorization)
    return await create_order(db, order, user_id)

@router.post("/create-full", response_model=Order)
async def create_new_order_full(order: OrderCreateNorm, db: AsyncSession = Depends(get_db), authorization: str = Header(None),):
    user_id = await check_user_auth_final(db, authorization)
    return await create_order_full(db, order, user_id)



@router.put("/{order_id}", response_model=OrderWithDetails)
async def update_order_endpoint(
        order_id: int, updated_order: OrderUpdate,
        db: AsyncSession = Depends(get_db),
        authorization: str = Header(None),
):
    # Вызов CRUD функции для обновления заказа
    user_id = await check_user_auth_final(db, authorization)
    return await update_order_full(db=db, order_id=order_id, updated_order=updated_order)

# @router.put("/{order_id}", response_model=Order)
# async def update_existing_order(order_id: int, order_update: OrderUpdate, db: AsyncSession = Depends(get_db)):
#     order = await update_order(db, order_id, order_update)
#     if order is None:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order


@router.delete("/{order_id}")
async def delete_existing_order(order_id: int,
                                db: AsyncSession = Depends(get_db),
                                authorization: str = Header(None),):
    user_id = await check_user_auth_final(db, authorization)
    order = await delete_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}

