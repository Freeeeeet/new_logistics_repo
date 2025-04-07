from crud.users_crud import check_auth
from fastapi import APIRouter, Depends, HTTPException, Header, status


async def check_user_auth_final(db, authorization):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    token = authorization[len("Bearer "):]
    authed_user = await check_auth(db=db, token=token)
    if not authed_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return authed_user.id

