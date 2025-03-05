from typing import List

from app.models import Booking, User
from app.services.admin_service import AdminService
from app.utils.security import get_admin_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/users", response_model=List[User])
def get_all_users(admin: User = Depends(get_admin_user)):
    return AdminService.get_all_users(admin)


@router.get("/bookings", response_model=List[Booking])
def get_all_bookings(admin: User = Depends(get_admin_user)):
    return AdminService.get_all_bookings(admin)


@router.delete("/user/{user_id}")
def delete_user(user_id: int, admin: User = Depends(get_admin_user)):
    return AdminService.delete_user(user_id, admin)


@router.delete("/booking/{booking_id}")
def delete_booking_admin(booking_id: int, admin: User = Depends(get_admin_user)):
    return AdminService.delete_booking(booking_id, admin)
