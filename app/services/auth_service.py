import logging

from app.database import get_session
from app.models import User
from app.utils.security import create_token, hash_password, verify_password
from fastapi import Depends, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import select

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def register_user(
        username: str, password: str, is_admin: bool, session=Depends(get_session)
    ):
        if session.exec(select(User).where(User.username == username)).first():
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(
            username=username,
            hashed_password=hash_password(password),
            is_admin=is_admin,
        )
        session.add(user)
        session.commit()
        return {"message": "User registered successfully"}

    @staticmethod
    @limiter.limit("5/minute")  # ✅ Prevent brute-force attacks
    def login_user(username: str, password: str, session=Depends(get_session)):
        user = session.exec(select(User).where(User.username == username)).first()
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(
                f"Failed login attempt for username: {username}"
            )  # ✅ Log failed attempts
            raise HTTPException(status_code=400, detail="Invalid username or password")
        return {"access_token": create_token(user), "token_type": "bearer"}
