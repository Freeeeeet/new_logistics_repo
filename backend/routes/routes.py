from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas import RouteCreate, Route
from crud.routes_crud import create_route, get_route, update_route, delete_route

router = APIRouter()

@router.post("/", response_model=Route)
async def create_route(route_data: RouteCreate, db: AsyncSession = Depends(get_db)):
    return await create_route(db, route_data)

@router.get("/{route_id}", response_model=Route)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    return await get_route(db, route_id)

@router.put("/{route_id}", response_model=Route)
async def update_route(route_id: int, route_data: RouteCreate, db: AsyncSession = Depends(get_db)):
    return await update_route(db, route_id, route_data)

@router.delete("/{route_id}")
async def delete_route(route_id: int, db: AsyncSession = Depends(get_db)):
    await delete_route(db, route_id)
    return {"message": "Route deleted successfully"}