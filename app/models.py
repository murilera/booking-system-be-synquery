from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)  # ✅ Indexed for faster queries
    hashed_password: str
    credits: int = 10
    is_admin: bool = False


class Booking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    name: str
    profession: str
    date: str = Field(index=True)  # ✅ Indexed for faster date filtering
    time: str
