from sqlalchemy.orm import Session
from models import Cargo
from schemas import CargoCreate, CargoUpdate


def create_cargo(db: Session, cargo: CargoCreate):
    db_cargo = Cargo(**cargo.dict())
    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)
    return db_cargo


def get_cargo(db: Session, cargo_id: int):
    return db.query(Cargo).filter(Cargo.id == cargo_id).first()


def get_cargos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cargo).offset(skip).limit(limit).all()


def update_cargo(db: Session, cargo_id: int, cargo_update: CargoUpdate):
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not db_cargo:
        return None

    for key, value in cargo_update.dict(exclude_unset=True).items():
        setattr(db_cargo, key, value)

    db.commit()
    db.refresh(db_cargo)
    return db_cargo


def delete_cargo(db: Session, cargo_id: int):
    db_cargo = db.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not db_cargo:
        return None

    db.delete(db_cargo)
    db.commit()
    return db_cargo