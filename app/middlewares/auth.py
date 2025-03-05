from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

from app.utils.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Security(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
