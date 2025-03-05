from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AIRequest(BaseModel):
    """Schema for AI booking requests"""

    user_input: str


class AIBookingResponse(BaseModel):
    """Schema for AI booking responses"""

    message: str
    action: Optional[str] = None
    booking_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
