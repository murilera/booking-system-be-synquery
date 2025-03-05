from fastapi import FastAPI

from app.routes import ai_booking, auth, bookings, technicians, users
from app.utils.database import seed_database

app = FastAPI()


app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(users.router)
app.include_router(ai_booking.router)
app.include_router(technicians.router)


@app.on_event("startup")
async def startup():
    """Called when FastAPI starts"""
    await seed_database()
