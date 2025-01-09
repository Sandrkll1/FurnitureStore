import os

import dotenv

dotenv.load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

DATABASE_URI = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

REDIS_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'

JWS_SECRET_KEY = os.getenv('JWS_SECRET_KEY')
JWS_ALGORITHM = os.getenv('JWS_ALGORITHM')
JWS_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWS_ACCESS_TOKEN_EXPIRE_MINUTES'))
JWS_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('JWS_REFRESH_TOKEN_EXPIRE_DAYS'))

MEDIA_PATH = "/data/media"
