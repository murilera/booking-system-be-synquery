from app.database import get_session
from app.models import Booking, User
from app.utils.security import get_admin_user
from fastapi import Depends, HTTPException
from sqlmodel import select


class AdminService:
    @staticmethod
    def get_all_users(
        admin: User = Depends(get_admin_user), session=Depends(get_session)
    ):
        """Retrieve all registered users (Admin-only)."""
        return session.exec(select(User)).all()

    @staticmethod
    def get_all_bookings(
        admin: User = Depends(get_admin_user), session=Depends(get_session)
    ):
        """Retrieve all bookings (Admin-only)."""
        return session.exec(select(Booking)).all()

    @staticmethod
    def delete_user(
        user_id: int,
        admin: User = Depends(get_admin_user),
        session=Depends(get_session),
    ):
        """Delete a user by ID (Admin-only)."""
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"message": "User deleted successfully"}

    @staticmethod
    def delete_booking(
        booking_id: int,
        admin: User = Depends(get_admin_user),
        session=Depends(get_session),
    ):
        """Delete a booking by ID (Admin-only)."""
        booking = session.get(Booking, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        session.delete(booking)
        session.commit()
        return {"message": "Booking deleted successfully"}
