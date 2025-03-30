from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models import Order, Client, Cargo, Route, OrderStatus, Payment, Warehouse
from schemas import OrderCreate, OrderUpdate, OrderCreateNorm, OrderWithDetails
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

    # Преобразуем результат в нужный формат
    return [
        {
            "order_id": order.order_id,
            "is_paid": order.is_paid,
            "client_name": order.client_name,
            "client_email": order.client_email,
            "order_status": order.order_status,
            "origin": order.origin,
            "destination": order.destination,
            "warehouse_name": order.warehouse_name,
            "warehouse_location": order.warehouse_location,
            "cargo_description": order.cargo_description,
            "cargo_weight": order.cargo_weight,
            "cargo_volume": order.cargo_volume,
        }
        for order in orders
    ]


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


async def update_order_full(db: AsyncSession, order_id: int, updated_order: OrderUpdate) -> OrderWithDetails:
    async with db.begin():  # Начинаем транзакцию
        # Загружаем заказ вместе с платежами
        result = await db.execute(
            select(Order)
            .options(
                selectinload(Order.payments),
                selectinload(Order.route),  # Явная загрузка маршрута
                selectinload(Order.warehouse),  # Явная загрузка склада
            )
            .where(Order.id == order_id)
        )
        db_order = result.scalar_one_or_none()

        if not db_order:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        # Обновляем клиента
        db_client = await db.get(Client, db_order.client_id)
        if db_client and any([updated_order.client_name, updated_order.client_email, updated_order.client_phone]):
            if updated_order.client_name:
                db_client.name = updated_order.client_name
            if updated_order.client_email:
                db_client.email = updated_order.client_email
            if updated_order.client_phone:
                db_client.phone = updated_order.client_phone

        # Обновляем груз
        db_cargo = await db.get(Cargo, db_order.cargo_id)
        if db_cargo and any([updated_order.cargo_description, updated_order.cargo_weight, updated_order.cargo_volume]):
            if updated_order.cargo_description:
                db_cargo.description = updated_order.cargo_description
            if updated_order.cargo_weight:
                db_cargo.weight = updated_order.cargo_weight
            if updated_order.cargo_volume:
                db_cargo.volume = updated_order.cargo_volume

        # Обновляем маршрут и склад
        if any([updated_order.route_id, updated_order.warehouse_id]):
            if updated_order.route_id:
                db_order.route_id = updated_order.route_id
            if updated_order.warehouse_id:
                db_order.warehouse_id = updated_order.warehouse_id

    await db.commit()
    await db.refresh(db_order)

    # Проверяем оплату
    is_paid = 1 if db_order.payments else 0  # payments уже загружены, ошибки не будет
    db_status = await db.get(OrderStatus, db_order.status_id)

    return OrderWithDetails(
        order_id=db_order.id,
        is_paid=is_paid,
        client_name=db_client.name if db_client else None,
        client_email=db_client.email if db_client else None,
        order_status=db_status.name if db_status else None,
        origin=db_order.route.origin,
        destination=db_order.route.destination,
        warehouse_name=db_order.warehouse.name if db_order.warehouse else None,
        warehouse_location=db_order.warehouse.location if db_order.warehouse else None,
        cargo_description=db_cargo.description if db_cargo else None,
        cargo_weight=db_cargo.weight if db_cargo else None,
        cargo_volume=db_cargo.volume if db_cargo else None,
    )



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
