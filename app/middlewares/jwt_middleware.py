from app.utils.security import SECRET_KEY, verify_token
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            try:
                verify_token(token, SECRET_KEY)
            except HTTPException as e:
                return HTTPException(status_code=e.status_code, detail=e.detail)
        response = await call_next(request)
        return response
