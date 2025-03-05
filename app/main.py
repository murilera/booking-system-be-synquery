import logging

from app.database import create_db_and_tables
from app.middlewares.jwt_middleware import JWTAuthMiddleware
from app.routes import admin_routes, auth_routes, booking_routes
from fastapi import FastAPI, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(HTTPException, _rate_limit_exceeded_handler)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.add_middleware(JWTAuthMiddleware)

# ✅ Register Routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(booking_routes.router, prefix="/booking", tags=["Booking"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
