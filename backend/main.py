from fastapi import FastAPI
from database import engine
from models import Base
from routes import orders

app = FastAPI(root_path="logistics/api")

app.include_router(orders.router, prefix="/orders", tags=["orders"])


# Создание таблиц при старте (только для отладки)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()
