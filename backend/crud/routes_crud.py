from sqlalchemy.ext.asyncio import AsyncSession
from models import Route as RouteModel
from schemas import RouteCreate
from fastapi import HTTPException

async def create_route(db: AsyncSession, route_data: RouteCreate):
    new_route = RouteModel(**route_data.dict())
    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)
    return new_route

async def get_route(db: AsyncSession, route_id: int):
    route = await db.get(RouteModel, route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

async def update_route(db: AsyncSession, route_id: int, route_data: RouteCreate):
    route = await get_route(db, route_id)
    for key, value in route_data.dict(exclude_unset=True).items():
        setattr(route, key, value)
    await db.commit()
    await db.refresh(route)
    return route

async def delete_route(db: AsyncSession, route_id: int):
    route = await get_route(db, route_id)
    await db.delete(route)
    await db.commit()