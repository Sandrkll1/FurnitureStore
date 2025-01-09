import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from database.service_manager import ServiceManager
import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.JWS_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    to_encode.update({"sub": str(to_encode.get("sub"))})
    encoded_jwt = jwt.encode(to_encode, config.JWS_SECRET_KEY, algorithm=config.JWS_ALGORITHM)
    return encoded_jwt


async def create_refresh_token(user_id: int):
    expires_delta = timedelta(days=config.JWS_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": str(user_id)}
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWS_SECRET_KEY, algorithm=config.JWS_ALGORITHM)
    return encoded_jwt


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config.JWS_SECRET_KEY, algorithms=[config.JWS_ALGORITHM])
        user_id: int = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="Invalid token")

        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def verify_refresh_token(token: str):
    try:
        manager = ServiceManager()
        payload = jwt.decode(token, config.JWS_SECRET_KEY, algorithms=[config.JWS_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_BAD_REQUEST, detail="Invalid refresh token")

        auth_record = await manager.auth.get(user_id=user_id, refresh_token=token)
        if auth_record is None or auth_record.denied:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

        return user_id
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from e


async def authenticate_user(email: str, password: str):
    manager = ServiceManager()
    user = await manager.user.get(email=email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user
