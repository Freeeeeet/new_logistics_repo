from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas import ClientCreate, Client, ClientUpdate
from crud.clients_crud import create_client, get_client, update_client, delete_client

router = APIRouter()

@router.post("/", response_model=Client)
async def create_client(client_data: ClientCreate, db: AsyncSession = Depends(get_db)):
    return await create_client(db, client_data)

@router.get("/{client_id}", response_model=Client)
async def get_client(client_id: int, db: AsyncSession = Depends(get_db)):
    return await get_client(db, client_id)

@router.put("/{client_id}", response_model=Client)
async def update_client(client_id: int, client_data: ClientUpdate, db: AsyncSession = Depends(get_db)):
    return await update_client(db, client_id, client_data)

@router.delete("/{client_id}")
async def delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    await delete_client(db, client_id)
    return {"message": "Client deleted successfully"}
