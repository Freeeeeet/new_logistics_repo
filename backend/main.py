from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import orders  # Подключаем другие маршруты

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
# app.include_router(clients.router, prefix="/clients", tags=["clients"])
# app.include_router(cargo.router, prefix="/cargo", tags=["cargo"])


# Создание таблиц при старте (только для отладки)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()
