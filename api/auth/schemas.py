from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class GetRefreshToken(BaseModel):
    refresh_token: str


class RefreshTokenRead(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
