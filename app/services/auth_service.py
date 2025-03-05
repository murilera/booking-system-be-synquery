from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User


async def authenticate_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user and user.password == password:
        return user
    return None
