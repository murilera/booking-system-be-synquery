from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import AuthToken
from app.services.auth_service import authenticate_user
from app.utils.database import get_db
from app.utils.security import create_access_token

router = APIRouter()


@router.post("/token")
async def login(
    payload: AuthToken,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(payload.email, payload.password, db)
    if not user:
        return {"error": "Invalid credentials"}
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
