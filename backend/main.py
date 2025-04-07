from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import orders, cargo, order_assignment, clients, routes, warehouses, users  # Подключаем другие маршруты

app = FastAPI(root_path="/logistics/api")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно заменить на список доверенных источников
    allow_credentials=True,
    allow_methods=["*"],  # Можно указать методы, если нужно ограничить
    allow_headers=["*"],  # Можно указать, какие заголовки разрешены
)

# Подключаем маршруты
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(cargo.router, prefix="/cargo", tags=["cargo"])
app.include_router(routes.router, prefix="/routes", tags=["routes"])
app.include_router(order_assignment.router, prefix="/order_assignments", tags=["Order Assignments"])
app.include_router(warehouses.router, prefix="/warehouses", tags=["warehouses"])
app.include_router(users.router, prefix="/users", tags=["users"])


# Создание таблиц при старте (только для отладки)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()
