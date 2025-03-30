from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Order, Client, Cargo, Route, OrderStatus
from schemas import OrderCreate, OrderUpdate, OrderCreateNorm
from fastapi import HTTPException

from datetime import datetime


async def get_all_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    return result.scalars().first()


async def create_order(db: AsyncSession, order_data: OrderCreate):
    # Создание нового клиента, если клиент передан как словарь
    client = await db.get(Client, order_data.client_id) if isinstance(order_data.client_id, int) else None
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    # Создание нового груза
    cargo = Cargo(**order_data.cargo.dict())
    db.add(cargo)
    await db.flush()

    # Создание нового маршрута
    route = Route(**order_data.route.dict())
    db.add(route)
    await db.flush()

    # Создание заказа с автоматически установленным статусом
    status = await db.get(OrderStatus, 1)  # предполагаем, что статус 1 — это первый статус
    new_order = Order(
        client_id=client.id,
        cargo_id=cargo.id,
        route_id=route.id,
        status_id=status.id
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order


async def create_order_full(db: AsyncSession, order: OrderCreateNorm):
    async with db.begin():  # Начинаем транзакцию
        # 1. Создаем нового клиента
        client = Client(
            name=order.client_name,
            email=order.client_email,
            phone=order.client_phone
        )
        db.add(client)

        # 2. Создаем новый груз
        cargo = Cargo(
            description=order.cargo_description,
            weight=int(order.cargo_weight),
            volume=int(order.cargo_volume)
        )
        db.add(cargo)

        # 3. Получаем статус заказа (например, 'В процессе')

        status = 1

        # 4. Создаем новый заказ
        order_data = Order(
            client_id=int(client.id),
            cargo_id=int(cargo.id),
            route_id=int(order.route_id),
            warehouse_id=int(order.warehouse_id),
            status_id=status,
            created_at=datetime.now()
        )
        db.add(order_data)

    await db.commit()

    return order_data


async def update_order(db: AsyncSession, order_id: int, order_update: OrderUpdate):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalars().first()
    if db_order:
        for key, value in order_update.dict().items():
            setattr(db_order, key, value)
        await db.commit()
        await db.refresh(db_order)
    return db_order


async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    db_order = result.scalars().first()
    if db_order:
        await db.delete(db_order)
        await db.commit()
    return db_order
