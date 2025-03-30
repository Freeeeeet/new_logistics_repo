from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Order, Client, Cargo, Route, OrderStatus, Payment, Warehouse
from schemas import OrderCreate, OrderUpdate, OrderCreateNorm
from fastapi import HTTPException

from datetime import datetime


async def get_all_orders(db: AsyncSession):
    result = await db.execute(
        select(
            Order.id.label("order_id"),
            Payment.id.label("is_paid"),
            Client.name.label("client_name"),
            Client.email.label("client_email"),
            OrderStatus.name.label("order_status"),
            Route.origin.label("origin"),
            Route.destination.label("destination"),
            Warehouse.name.label("warehouse_name"),
            Warehouse.location.label("warehouse_location"),
            Cargo.description.label("cargo_description"),
            Cargo.weight.label("cargo_weight"),
            Cargo.volume.label("cargo_volume"),
        )
        .select_from(Order)
        .outerjoin(Payment, Payment.order_id == Order.id)
        .join(Client, Order.client_id == Client.id)
        .join(OrderStatus, Order.status_id == OrderStatus.id)
        .join(Route, Order.route_id == Route.id)
        .join(Warehouse, Order.warehouse_id == Warehouse.id)
        .join(Cargo, Order.cargo_id == Cargo.id)
        .order_by(Order.id.desc())
    )
    # Скалярный результат преобразуем в список словарей
    orders = result.fetchall()
    return [dict(order) for order in orders]


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
            weight=order.cargo_weight,
            volume=order.cargo_volume
        )
        db.add(cargo)

        # 3. Принудительно "флешим" транзакцию, чтобы получить ID для client и cargo
        await db.flush()

        # 4. Получаем статус заказа (например, 'В процессе')
        status = 1

        # 5. Создаем новый заказ
        order_data = Order(
            client_id=client.id,
            cargo_id=cargo.id,
            route_id=order.route_id,
            warehouse_id=order.warehouse_id,
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
