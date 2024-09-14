from pydantic import BaseModel, EmailStr


class LoginDto(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenDto(BaseModel):
    refresh: str