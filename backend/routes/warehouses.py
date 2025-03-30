from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import Warehouse, WarehouseCreate, WarehouseUpdate
from crud.warehouses_crud import get_all_warehouses, get_warehouse_by_id, create_warehouse, update_warehouse, delete_warehouse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Warehouse])
async def read_warehouses(db: AsyncSession = Depends(get_db)):
    return await get_all_warehouses(db)

@router.get("/{warehouse_id}", response_model=Warehouse)
async def read_warehouse(warehouse_id: int, db: AsyncSession = Depends(get_db)):
    warehouse = await get_warehouse_by_id(db, warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@router.post("/", response_model=Warehouse)
async def create_new_warehouse(warehouse: WarehouseCreate, db: AsyncSession = Depends(get_db)):
    return await create_warehouse(db, warehouse)

@router.put("/{warehouse_id}", response_model=Warehouse)
async def update_existing_warehouse(warehouse_id: int, warehouse_update: WarehouseUpdate, db: AsyncSession = Depends(get_db)):
    warehouse = await update_warehouse(db, warehouse_id, warehouse_update)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@router.delete("/{warehouse_id}")
async def delete_existing_warehouse(warehouse_id: int, db: AsyncSession = Depends(get_db)):
    warehouse = await delete_warehouse(db, warehouse_id)
    if warehouse is None:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return {"detail": "Warehouse deleted"}