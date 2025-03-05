from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.middlewares.auth import get_current_user
from app.models.booking import Booking
from app.schemas.booking import BookingCreate
from app.utils.database import get_db

router = APIRouter()


@router.get("/bookings/")
async def list_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking))
    return result.scalars().all()


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    """Fetch a single booking by ID"""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.post("/bookings/")
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]

    end_time = booking_data.scheduled_at + timedelta(hours=1)
    conflicting_booking = await db.execute(
        select(Booking).where(
            Booking.technician_name == booking_data.technician_name,
            Booking.scheduled_at.between(booking_data.scheduled_at, end_time),
        )
    )
    if conflicting_booking.scalars().first():
        raise HTTPException(status_code=400, detail="Already booked at this time")

    new_booking = Booking(
        user_id=user_id,
        book_id=booking_data.book_id,
        technician_name=booking_data.technician_name,
        profession=booking_data.profession,
        scheduled_at=booking_data.scheduled_at,
    )
    db.add(new_booking)
    await db.commit()
    return {"success": True, "message": "Booked"}


@router.delete("/bookings/{booking_id}")
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a booking by ID"""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    await db.delete(booking)
    await db.commit()
    return {"success": True, "message": "Booking deleted successfully"}
