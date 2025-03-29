from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from models import Cargo
from schemas import CargoCreate, CargoUpdate


async def create_cargo(db: AsyncSession, cargo: CargoCreate):
    db_cargo = Cargo(**cargo.dict())
    db.add(db_cargo)
    await db.commit()
    await db.refresh(db_cargo)
    return db_cargo


async def get_cargo(db: AsyncSession, cargo_id: int):
    result = await db.execute(select(Cargo).filter(Cargo.id == cargo_id))
    cargo = result.scalars().first()
    return cargo


async def get_cargos(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Cargo).offset(skip).limit(limit))
    return result.scalars().all()


async def update_cargo(db: AsyncSession, cargo_id: int, cargo_update: CargoUpdate):
    result = await db.execute(select(Cargo).filter(Cargo.id == cargo_id))
    db_cargo = result.scalars().first()

    if not db_cargo:
        return None

    for key, value in cargo_update.dict(exclude_unset=True).items():
        setattr(db_cargo, key, value)

    await db.commit()
    await db.refresh(db_cargo)
    return db_cargo


async def delete_cargo(db: AsyncSession, cargo_id: int):
    result = await db.execute(select(Cargo).filter(Cargo.id == cargo_id))
    db_cargo = result.scalars().first()

    if not db_cargo:
        return None

    await db.delete(db_cargo)
    await db.commit()
    return db_cargo