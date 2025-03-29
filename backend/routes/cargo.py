from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Cargo)
def create_cargo(cargo: schemas.CargoCreate, db: Session = Depends(get_db)):
    return crud.create_cargo(db=db, cargo=cargo)


@router.get("/{cargo_id}", response_model=schemas.Cargo)
def read_cargo(cargo_id: int, db: Session = Depends(get_db)):
    cargo = crud.get_cargo(db=db, cargo_id=cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router.get("/", response_model=list[schemas.Cargo])
def read_cargos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cargos(db=db, skip=skip, limit=limit)


@router.put("/{cargo_id}", response_model=schemas.Cargo)
def update_cargo(cargo_id: int, cargo_update: schemas.CargoUpdate, db: Session = Depends(get_db)):
    cargo = crud.update_cargo(db=db, cargo_id=cargo_id, cargo_update=cargo_update)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo


@router.delete("/{cargo_id}", response_model=schemas.Cargo)
def delete_cargo(cargo_id: int, db: Session = Depends(get_db)):
    cargo = crud.delete_cargo(db=db, cargo_id=cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo not found")
    return cargo