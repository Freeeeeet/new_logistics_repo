from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import OrderAssignment
from schemas import OrderAssignmentCreate, OrderAssignmentUpdate


async def create_order_assignment(db: AsyncSession, assignment: OrderAssignmentCreate):
    db_assignment = OrderAssignment(**assignment.dict())
    db.add(db_assignment)
    await db.commit()
    await db.refresh(db_assignment)
    return db_assignment


async def get_order_assignment(db: AsyncSession, assignment_id: int):
    result = await db.execute(select(OrderAssignment).filter(OrderAssignment.id == assignment_id))
    return result.scalars().first()


async def get_order_assignments(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(OrderAssignment).offset(skip).limit(limit))
    return result.scalars().all()


async def update_order_assignment(db: AsyncSession, assignment_id: int, assignment_update: OrderAssignmentUpdate):
    result = await db.execute(select(OrderAssignment).filter(OrderAssignment.id == assignment_id))
    db_assignment = result.scalars().first()

    if not db_assignment:
        return None

    for key, value in assignment_update.dict(exclude_unset=True).items():
        setattr(db_assignment, key, value)

    await db.commit()
    await db.refresh(db_assignment)
    return db_assignment


async def delete_order_assignment(db: AsyncSession, assignment_id: int):
    result = await db.execute(select(OrderAssignment).filter(OrderAssignment.id == assignment_id))
    db_assignment = result.scalars().first()

    if not db_assignment:
        return None

    await db.delete(db_assignment)
    await db.commit()
    return db_assignment