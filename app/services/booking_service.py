import logging

from app.database import get_session
from app.models import Booking, User
from fastapi import Depends, HTTPException
from sqlmodel import select

logger = logging.getLogger(__name__)


class BookingService:
    @staticmethod
    def create_booking(
        user: User,
        name: str,
        profession: str,
        date: str,
        time: str,
        session=Depends(get_session),
    ):
        if user.credits <= 0:
            raise HTTPException(
                status_code=403, detail="Insufficient credits. Please recharge."
            )

        # ✅ Prevent duplicate booking
        existing_booking = session.exec(
            select(Booking).where(
                (Booking.user_id == user.id)
                & (Booking.date == date)
                & (Booking.time == time)
            )
        ).first()
        if existing_booking:
            raise HTTPException(
                status_code=400, detail="You already have a booking at this time."
            )

        user.credits -= 1
        booking = Booking(
            user_id=user.id, name=name, profession=profession, date=date, time=time
        )
        session.add(booking)
        session.commit()
        return {"message": "Booking successful", "remaining_credits": user.credits}

    @staticmethod
    def delete_booking(user: User, booking_id: int, session=Depends(get_session)):
        booking = session.get(Booking, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        if not user.is_admin and booking.user_id != user.id:
            raise HTTPException(status_code=403, detail="Permission denied")

        session.delete(booking)
        session.commit()
        logger.info(
            f"User {user.username} deleted booking {booking_id}"
        )  # ✅ Log booking deletions
        return {"message": "Booking deleted successfully"}
