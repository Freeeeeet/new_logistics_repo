from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas import ClientCreate, Client, ClientUpdate
from crud.clients_crud import create_client, get_clients, get_client, update_client, delete_client
from utils.user_auth import check_user_auth_final

router = APIRouter()

@router.post("/", response_model=Client)
async def create_client_endpoint(client_data: ClientCreate, db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    user_id = await check_user_auth_final(db, authorization)
    return await create_client(db, client_data)

@router.get("/", response_model=list[Client])
async def get_clients_endpoint(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    user_id = await check_user_auth_final(db, authorization)
    return await get_clients(db, offset, limit)

@router.get("/{client_id}", response_model=Client)
async def get_client_endpoint(client_id: int, db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    user_id = await check_user_auth_final(db, authorization)
    return await get_client(db, client_id)

@router.put("/{client_id}", response_model=Client)
async def update_client_endpoint(client_id: int, client_data: ClientUpdate, db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    user_id = await check_user_auth_final(db, authorization)
    return await update_client(db, client_id, client_data)

@router.delete("/{client_id}")
async def delete_client_endpoint(client_id: int, db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    user_id = await check_user_auth_final(db, authorization)
    await delete_client(db, client_id)
    return {"message": "Client deleted successfully"}

