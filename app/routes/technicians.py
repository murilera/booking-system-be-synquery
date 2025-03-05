from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.middlewares.auth import get_current_user
from app.models.technician import Technician
from app.schemas.technician import TechnicianCreate, TechnicianResponse
from app.utils.database import get_db

router = APIRouter()


@router.post("/technicians/", response_model=TechnicianResponse)
async def create_technician(
    technician_data: TechnicianCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new technician."""
    existing_technician = await db.execute(
        select(Technician).where(Technician.name == technician_data.name)
    )

    if existing_technician.scalars().first():
        raise HTTPException(status_code=400, detail="Technician already exists.")

    new_technician = Technician(
        name=technician_data.name, profession=technician_data.profession
    )
    db.add(new_technician)
    await db.commit()
    await db.refresh(new_technician)
    return new_technician


@router.get("/technicians/", response_model=list[TechnicianResponse])
async def get_all_technicians(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Retrieve all technicians."""
    result = await db.execute(select(Technician))
    return result.scalars().all()


@router.delete("/technicians/{technician_id}")
async def delete_technician(
    technician_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a technician by ID."""
    technician = await db.get(Technician, technician_id)
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")

    await db.delete(technician)
    await db.commit()
    return {"message": f"Technician {technician_id} deleted successfully"}
