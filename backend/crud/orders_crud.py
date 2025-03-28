from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Order
from schemas import OrderCreate, OrderUpdate


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