from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Warehouse
from schemas import WarehouseCreate, WarehouseUpdate

async def get_all_warehouses(db: AsyncSession):
    result = await db.execute(select(Warehouse))
    return result.scalars().all()

async def get_warehouse_by_id(db: AsyncSession, warehouse_id: int):
    result = await db.execute(select(Warehouse).filter(Warehouse.id == warehouse_id))
    return result.scalar_one_or_none()

async def create_warehouse(db: AsyncSession, warehouse: WarehouseCreate):
    db_warehouse = Warehouse(name=warehouse.name, location=warehouse.location)
    db.add(db_warehouse)
    await db.commit()
    await db.refresh(db_warehouse)
    return db_warehouse

async def update_warehouse(db: AsyncSession, warehouse_id: int, warehouse_update: WarehouseUpdate):
    db_warehouse = await get_warehouse_by_id(db, warehouse_id)
    if db_warehouse:
        db_warehouse.name = warehouse_update.name
        db_warehouse.location = warehouse_update.location
        await db.commit()
        await db.refresh(db_warehouse)
        return db_warehouse
    return None

async def delete_warehouse(db: AsyncSession, warehouse_id: int):
    db_warehouse = await get_warehouse_by_id(db, warehouse_id)
    if db_warehouse:
        await db.delete(db_warehouse)
        await db.commit()
        return db_warehouse
    return None