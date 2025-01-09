from datetime import datetime
from http.client import HTTPException

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_cache.decorator import cache

from api.dependencies import get_current_user, get_service_manager
from api.profile.schemas import UserProfileResponse, UserProfileUpdate, RoleResponse
from database.models.user import User
from database.service_manager import ServiceManager

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/profile", response_model=UserProfileResponse)
@cache(expire=15)
async def get_user_profile(user: User = Depends(get_current_user)):
    return UserProfileResponse(
        name=user.name,
        email=user.email,
        birthday=user.birthday.isoformat() if user.birthday else None,
        image_url=user.image,
        role=RoleResponse.model_validate(user.role, from_attributes=True)
    )


@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
        user_update: UserProfileUpdate,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager)
):
    user.name = user_update.name
    if user_update.birthday:
        try:
            user.birthday = datetime.fromisoformat(user_update.birthday)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    await manager.user.update(user.user_id, name=user_update.name, birthday=user.birthday)
    return UserProfileResponse.model_validate(user, from_attributes=True)
