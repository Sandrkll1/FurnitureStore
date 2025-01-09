from fastapi import HTTPException, status, Security, Depends
from api.auth.controller import oauth2_scheme, verify_token
from database.models.user import RoleEnum
from database.service_manager import ServiceManager


MANAGER = ServiceManager()


async def get_service_manager():
    global MANAGER
    if not MANAGER:
        MANAGER = ServiceManager()
    return MANAGER


async def get_current_user(token: str = Security(oauth2_scheme), manager: ServiceManager = Depends(get_service_manager)):
    user_id = await verify_token(token)
    user = await manager.user.get(user_id=user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user


async def get_current_admin(token: str = Security(oauth2_scheme), manager: ServiceManager = Depends(get_service_manager)):
    user_id = await verify_token(token)

    user = await manager.user.get(user_id=user_id)
    role = await manager.role.get(primary_key_value=user.role_id)

    if user is None or role.name != RoleEnum.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user

