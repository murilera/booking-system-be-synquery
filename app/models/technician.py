from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    profession = Column(String, index=True)

    bookings = relationship("Booking", back_populates="technician")
