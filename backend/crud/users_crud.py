from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

import models
import schemas
from utils.security import hash_password, verify_password, create_access_token


async def create_user(db: AsyncSession, user: schemas.UserCreateRequest):
    try:
        password_hash = hash_password(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            password_hash=password_hash
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding user to the database."
        )


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).where(models.User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(models.User).where(models.User.email == email)
    )
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


async def create_token(db: AsyncSession, user_id: int):
    try:
        access_token = create_access_token()
        db_token = models.Token(
            user_id=user_id,
            token=access_token,
        )
        db.add(db_token)
        await db.commit()
        await db.refresh(db_token)
        print(f"Token for user {user_id} added to database correctly, returning user")
        return access_token
    except Exception as e:
        await db.rollback()
        print(f"An error occurred while adding user to DB. {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding user to the database."
        )


async def check_auth(db: AsyncSession, token: str):
    try:
        result = await db.execute(
            select(models.Token).where(models.Token.token == token)
        )
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"An error occurred while checking user token: {e}")
        return None

