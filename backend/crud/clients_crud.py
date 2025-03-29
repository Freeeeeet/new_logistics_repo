from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Client
from schemas import ClientCreate, ClientUpdate
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

async def create_client(db: AsyncSession, client_data: ClientCreate):
    new_client = Client(**client_data.dict())
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client

async def get_client(db: AsyncSession, client_id: int):
    query = select(Client).filter(Client.id == client_id)
    result = await db.execute(query)
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

async def get_clients(db: AsyncSession, offset: int = 0, limit: int = 10):
    result = await db.execute(select(Client).offset(offset).limit(limit))
    clients = result.scalars().all()
    return clients


async def update_client(db: AsyncSession, client_id: int, client_data: ClientUpdate):
    client = await get_client(db, client_id)
    for key, value in client_data.dict(exclude_unset=True).items():
        setattr(client, key, value)
    await db.commit()
    await db.refresh(client)
    return client

async def delete_client(db: AsyncSession, client_id: int):
    client = await get_client(db, client_id)
    await db.delete(client)
    await db.commit()