from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.middlewares.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.database import get_db

router = APIRouter()


@router.get("/users/")
async def list_users(
    db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    """Fetch all users"""
    result = await db.execute(select(User))
    return result.scalars().all()


@router.post("/users/")
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new user"""
    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user_data.name, email=user_data.email, password=user_data.password
    )
    db.add(new_user)
    await db.commit()
    return {"success": True, "message": "User created successfully"}


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Fetch a single user by ID"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a user by ID"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"success": True, "message": "User deleted successfully"}
