from app.services.auth_service import AuthService
from app.utils.security import oauth2_scheme, refresh_access_token
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register")
def register(username: str, password: str, is_admin: bool = False):
    return AuthService.register_user(username, password, is_admin)


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return AuthService.login_user(form_data.username, form_data.password)


@router.post("/refresh")
def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
    """🔄 Refresh Access Token Using a Valid Refresh Token"""
    return refresh_access_token(refresh_token)
