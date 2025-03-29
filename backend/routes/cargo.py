from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud.cargo_crud as crud
import schemas
from database import get_db

router = APIRouter(prefix="/cargo", tags=["Cargo"])


@router.post("/", response_model=schemas.Cargo)
async def create_cargo(cargo: schemas.CargoCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_cargo(db=db, cargo=cargo)


@router.get("/{cargo_id}", response_model=schemas.Cargo)
async def read_cargo(cargo_id: int, db: AsyncSession = Depends(get_db)):
    cargo = await crud.get_cargo(db=db, cargo_id=cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router.get("/", response_model=list[schemas.Cargo])
async def read_cargos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_cargos(db=db, skip=skip, limit=limit)


@router.put("/{cargo_id}", response_model=schemas.Cargo)
async def update_cargo(cargo_id: int, cargo_update: schemas.CargoUpdate, db: AsyncSession = Depends(get_db)):
    cargo = await crud.update_cargo(db=db, cargo_id=cargo_id, cargo_update=cargo_update)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router.delete("/{cargo_id}", response_model=schemas.Cargo)
async def delete_cargo(cargo_id: int, db: AsyncSession = Depends(get_db)):
    cargo = await crud.delete_cargo(db=db, cargo_id=cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo