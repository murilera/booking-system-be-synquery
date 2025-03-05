from typing import List

from app.models import Booking, User
from app.services.booking_service import BookingService
from app.utils.security import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/book")
def create_booking(
    name: str,
    profession: str,
    date: str,
    time: str,
    user: User = Depends(get_current_user),
):
    return BookingService.create_booking(user, name, profession, date, time)


@router.get("/bookings", response_model=List[Booking])
def get_bookings():
    return BookingService.get_all_bookings()


@router.delete("/booking/{booking_id}")
def delete_booking(booking_id: int, user: User = Depends(get_current_user)):
    return BookingService.delete_booking(user, booking_id)
