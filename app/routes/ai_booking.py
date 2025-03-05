from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.middlewares.auth import get_current_user
from app.models.booking import Booking
from app.models.technician import Technician
from app.schemas.ai_booking import AIBookingResponse, AIRequest
from app.utils.database import get_db
from app.utils.openai_helper import get_openai_response

router = APIRouter()


@router.post("/ai/bookings/", response_model=AIBookingResponse)
async def process_natural_language_booking(
    request: AIRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Process AI booking requests, including creating, checking, and canceling bookings."""
    user_id = current_user["user_id"]
    user_input = request.user_input

    ai_response = get_openai_response(user_input)

    action = ai_response.get("action")
    profession = ai_response.get("profession")
    booking_id = ai_response.get("booking_id")
    date_str = ai_response.get("date")

    if action == "check_booking":
        user_bookings = await db.execute(
            select(Booking).where(Booking.user_id == user_id)
        )
        bookings = user_bookings.scalars().all()

        if not bookings:
            return AIBookingResponse(message="You have no scheduled bookings.")

        booking_messages = [
            f"Booking ID {b.id}: {b.profession} on {b.scheduled_at.strftime('%A at %I:%M %p')}"
            for b in bookings
        ]

        return AIBookingResponse(
            message="Your bookings: " + " || ".join(booking_messages),
            action="check_booking",
        )

    elif action == "cancel":
        if not booking_id:
            return AIBookingResponse(
                message="Please provide a valid booking ID to cancel."
            )

        booking = await db.get(Booking, booking_id)
        if not booking or booking.user_id != user_id:
            return AIBookingResponse(
                message="Booking not found or does not belong to you."
            )

        await db.delete(booking)
        await db.commit()
        return AIBookingResponse(
            message=f"Booking ID {booking_id} has been canceled.", action="cancel"
        )

    elif action == "book":
        now = datetime.now()

        if "tomorrow" in user_input.lower():
            requested_date = now.date() + timedelta(days=1)
        elif date_str:
            try:
                requested_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return AIBookingResponse(
                    message="Invalid date format. Please use YYYY-MM-DD."
                )
        else:
            return AIBookingResponse(message="Please specify a valid date.")

        start_hour = max(9, now.hour + 1) if requested_date == now.date() else 9

        available_tech_query = await db.execute(
            select(Technician).where(Technician.profession.ilike(f"%{profession}%"))
        )
        available_technicians = available_tech_query.scalars().all()

        if not available_technicians:
            return AIBookingResponse(message=f"No {profession}s are available.")

        for technician in available_technicians:
            for hour in range(start_hour, 18):
                scheduled_at = datetime.combine(
                    requested_date, datetime.min.time()
                ) + timedelta(hours=hour)

                existing_booking = await db.execute(
                    select(Booking).where(
                        Booking.technician_id == technician.id,
                        Booking.scheduled_at == scheduled_at,
                    )
                )

                if not existing_booking.scalars().first():
                    new_booking = Booking(
                        user_id=user_id,
                        technician_id=technician.id,
                        profession=profession,
                        scheduled_at=scheduled_at,
                    )
                    db.add(new_booking)
                    await db.commit()

                    return AIBookingResponse(
                        message=f"Booking confirmed with {technician.name} ({profession}) on {scheduled_at.strftime('%A at %I:%M %p')}",
                        booking_id=new_booking.id,
                        scheduled_at=scheduled_at,
                    )

        return AIBookingResponse(
            message=f"All {profession}s are fully booked for {requested_date.strftime('%A, %B %d')}. Please try another day."
        )

    return AIBookingResponse(message="I didn't understand your request.")
