from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.booking import Booking
from app.models.technician import Technician
from app.models.user import User

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/postgres"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def seed_database():
    """Seed the database with initial data"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # ✅ Seed Users
        existing_users = await session.execute(select(User))
        if not existing_users.scalars().all():
            users = [
                User(
                    name="Alice Doe",
                    email="alice@example.com",
                    password="securepassword",
                ),
                User(
                    name="Bob Smith", email="bob@example.com", password="securepassword"
                ),
            ]
            session.add_all(users)
            await session.commit()

        # ✅ Seed Technicians
        existing_technicians = await session.execute(select(Technician))
        if not existing_technicians.scalars().all():
            technicians = [
                Technician(name="John Waterman", profession="Plumber"),
                Technician(name="Jane Voltage", profession="Electrician"),
                Technician(name="Greg Sparks", profession="Welder"),
            ]
            session.add_all(technicians)
            await session.commit()

        # ✅ Seed Bookings
        user1 = await session.execute(
            select(User).where(User.email == "alice@example.com")
        )
        user2 = await session.execute(
            select(User).where(User.email == "bob@example.com")
        )
        tech1 = await session.execute(
            select(Technician).where(Technician.name == "John Waterman")
        )
        tech2 = await session.execute(
            select(Technician).where(Technician.name == "Jane Voltage")
        )
        tech3 = await session.execute(
            select(Technician).where(Technician.name == "Greg Sparks")
        )

        user1 = user1.scalars().first()
        user2 = user2.scalars().first()
        tech1 = tech1.scalars().first()
        tech2 = tech2.scalars().first()
        tech3 = tech3.scalars().first()

        if user1 and user2 and tech1 and tech2 and tech3:
            existing_bookings = await session.execute(select(Booking))
            if not existing_bookings.scalars().all():
                bookings = [
                    Booking(
                        user_id=user1.id,
                        technician_id=tech1.id,
                        profession="Plumber",
                        scheduled_at=datetime(2022, 10, 15, 10, 0),
                    ),
                    Booking(
                        user_id=user2.id,
                        technician_id=tech2.id,
                        profession="Electrician",
                        scheduled_at=datetime(2022, 10, 16, 18, 0),
                    ),
                    Booking(
                        user_id=user1.id,
                        technician_id=tech3.id,
                        profession="Welder",
                        scheduled_at=datetime(2022, 10, 18, 11, 0),
                    ),
                ]
                session.add_all(bookings)
                await session.commit()
