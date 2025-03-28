from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Order, Client, Cargo
from schemas import OrderCreate, OrderResponse

router = APIRouter()

@router.post("/api/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = Order(client_id=order.client_id, cargo_id=order.cargo_id)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/api/orders-with-client-cargo")
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order.id, Client.name, Cargo.description)
        .join(Client, Order.client_id == Client.id)
        .join(Cargo, Order.cargo_id == Cargo.id)
    )
    orders = result.all()
    return {"orders": [{"id": o[0], "client": o[1], "cargo": o[2]} for o in orders]}