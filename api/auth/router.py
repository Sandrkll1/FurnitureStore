from fastapi import APIRouter, HTTPException, status, Depends
from database.service_manager import ServiceManager
from .controller import create_access_token, create_refresh_token, verify_refresh_token, authenticate_user, pwd_context
from .schemas import UserCreate, UserLogin, GetRefreshToken, RefreshTokenRead
from api.dependencies import get_service_manager


router = APIRouter()


@router.post("/auth", response_model=RefreshTokenRead)
async def login_for_access_token(user_auth: UserLogin, manager: ServiceManager = Depends(get_service_manager)):
    user = await authenticate_user(user_auth.email, user_auth.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await create_access_token(data={"sub": user.user_id})
    refresh_token = await create_refresh_token(user.user_id)

    await manager.auth.create(user_id=user.user_id, refresh_token=refresh_token)

    return RefreshTokenRead(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/register")
async def register_user(user: UserCreate, manager: ServiceManager = Depends(get_service_manager)):
    stmt = await manager.user.get(email=user.email)

    if stmt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = await manager.user.create(
        name=user.name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )

    access_token = await create_access_token(data={"sub": new_user.user_id})
    refresh_token = await create_refresh_token(new_user.user_id)

    await manager.auth.create(user_id=new_user.user_id, refresh_token=refresh_token)

    return RefreshTokenRead(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/token/refresh", response_model=RefreshTokenRead)
async def refresh_access_token(rt: GetRefreshToken, manager: ServiceManager = Depends(get_service_manager)):
    user_id = await verify_refresh_token(rt.refresh_token)

    await manager.auth.mark_denied(refresh_token=rt.refresh_token)
    user = await manager.user.get(user_id=user_id)

    new_access_token = await create_access_token(data={"sub": str(user_id)})
    new_refresh_token = await create_refresh_token(user_id=user_id)

    await manager.auth.create(user_id=user.user_id, refresh_token=new_refresh_token)
    return RefreshTokenRead(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
