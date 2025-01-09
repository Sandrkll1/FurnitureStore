from datetime import datetime

from pydantic import BaseModel


class RoleResponse(BaseModel):
    role_id: int
    name: str


class UserProfileResponse(BaseModel):
    name: str
    email: str
    birthday: datetime | None = None
    image_url: str | None = None
    role: RoleResponse


class UserProfileUpdate(BaseModel):
    name: str
    birthday: str | None = None
