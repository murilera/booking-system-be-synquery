from datetime import datetime, timedelta

import bcrypt
import jwt
from app.database import get_session
from app.models import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

# JWT Config
SECRET_KEY = "supersecretkey"
REFRESH_SECRET_KEY = "refreshsupersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 hours
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Password Hashing
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_token(user: User):
    expire = datetime.utcnow() + timedelta(hours=1)  # ✅ Token expires in 1 hours
    payload = {"sub": user.username, "is_admin": user.is_admin, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user: User):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user.username, "is_admin": user.is_admin, "exp": expire}
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def refresh_access_token(refresh_token: str):
    payload = verify_token(refresh_token, REFRESH_SECRET_KEY)
    username = payload.get("sub")
    with get_session() as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return {"access_token": create_token(user), "token_type": "bearer"}


# Retrieve Current User from JWT Token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        with get_session() as session:
            user = session.exec(select(User).where(User.username == username)).first()
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Ensure User is Admin
def get_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
