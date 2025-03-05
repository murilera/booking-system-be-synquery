from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    technician_id = Column(Integer, ForeignKey("technicians.id"))
    profession = Column(String, index=True)
    scheduled_at = Column(DateTime, unique=True, index=True)

    technician = relationship("Technician", back_populates="bookings")
