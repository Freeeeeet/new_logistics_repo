from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Route
from schemas import RouteCreate
from fastapi import HTTPException

async def create_route(db: AsyncSession, route_data: RouteCreate):
    new_route = Route(**route_data.dict())
    db.add(new_route)
    await db.commit()
    await db.refresh(new_route)
    return new_route

async def get_route(db: AsyncSession, route_id: int):
    route = await db.get(Route, route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

async def get_routes(db: AsyncSession, offset: int = 0, limit: int = 10):
    result = await db.execute(select(Route).order_by(Route.id.desc()).offset(offset).limit(limit))
    routes = result.scalars().all()
    return routes

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