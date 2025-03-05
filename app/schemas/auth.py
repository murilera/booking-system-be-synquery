from pydantic import BaseModel, EmailStr


class AuthToken(BaseModel):
    email: EmailStr
    password: str
