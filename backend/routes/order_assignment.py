from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud.order_assignment_crud as crud
import schemas
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.OrderAssignment)
async def create_order_assignment(
    assignment: schemas.OrderAssignmentCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_order_assignment(db=db, assignment=assignment)


@router.get("/{assignment_id}", response_model=schemas.OrderAssignment)
async def read_order_assignment(assignment_id: int, db: AsyncSession = Depends(get_db)):
    assignment = await crud.get_order_assignment(db=db, assignment_id=assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Order Assignment not found")
    return assignment


@router.get("/", response_model=list[schemas.OrderAssignment])
async def read_order_assignments(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_order_assignments(db=db, skip=skip, limit=limit)


@router.put("/{assignment_id}", response_model=schemas.OrderAssignment)
async def update_order_assignment(
    assignment_id: int, assignment_update: schemas.OrderAssignmentUpdate, db: AsyncSession = Depends(get_db)
):
    assignment = await crud.update_order_assignment(db=db, assignment_id=assignment_id, assignment_update=assignment_update)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Order Assignment not found")
    return assignment


@router.delete("/{assignment_id}", response_model=schemas.OrderAssignment)
async def delete_order_assignment(assignment_id: int, db: AsyncSession = Depends(get_db)):
    assignment = await crud.delete_order_assignment(db=db, assignment_id=assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Order Assignment not found")
    return assignment
