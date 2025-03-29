from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Order, Client, Cargo, Route
from schemas import OrderCreate, OrderUpdate, OrderCreateFull


async def get_all_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def get_order_by_id(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    return result.scalars().first()


async def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


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

async def create_order_full(db: AsyncSession, order_data: OrderCreateFull):
    # Проверяем клиента
    if isinstance(order_data.client, int):
        client = await db.get(Client, order_data.client)
        if not client:
            raise ValueError("Клиент с таким ID не найден")
    else:
        client = Client(**order_data.client.model_dump())
        db.add(client)
        await db.flush()  # Получаем client.id

    # Создаем новый груз
    cargo = Cargo(**order_data.cargo.model_dump())
    db.add(cargo)
    await db.flush()  # Получаем cargo.id

    # Проверяем маршрут
    if isinstance(order_data.route, int):
        route = await db.get(Route, order_data.route)
        if not route:
            raise ValueError("Маршрут с таким ID не найден")
    else:
        route = Route(**order_data.route.model_dump())
        db.add(route)
        await db.flush()  # Получаем route.id

    # Создаем заказ
    new_order = Order(
        client_id=client.id,
        cargo_id=cargo.id,
        warehouse_id=order_data.warehouse_id,
        route_id=route.id,
        status_id=1,  # Всегда 1 при создании
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return new_order