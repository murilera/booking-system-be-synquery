from pydantic import BaseModel


class TechnicianCreate(BaseModel):
    """Schema for creating a technician."""

    name: str
    profession: str


class TechnicianResponse(BaseModel):
    """Schema for returning technician data."""

    id: int
    name: str
    profession: str

    class Config:
        orm_mode = True
