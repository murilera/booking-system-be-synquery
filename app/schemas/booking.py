from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    book_id: int
    technician_name: str
    profession: str
    scheduled_at: datetime
