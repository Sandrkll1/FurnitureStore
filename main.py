import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator
import time

from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

import api
import config
import middleware
from database.base import initialize_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    r = Redis.from_url(url=config.REDIS_URI)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")

    await init()

    yield

    await r.close()


async def init():
    logger.info("Waiting for database to be ready...")
    await asyncio.sleep(5)
    await initialize_database()


app = FastAPI(title="Jewelry", root_path="/api", docs_url=None, redoc_url=None, lifespan=lifespan)

middleware.setup(app)
api.setup(app)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Логируем метод и путь запроса
    print(f"Запрос: {request.method} {request.url}")

    # Логируем заголовки запроса
    headers = dict(request.headers)
    print(f"Заголовки: {headers}")

    # Логируем тело запроса (если есть)
    try:
        body = await request.json()
        print(f"Тело запроса: {body}")
    except Exception:
        body = None
        print("Тело запроса отсутствует или не может быть прочитано")

    # Время начала обработки запроса
    start_time = time.time()

    # Передаем управление следующему обработчику
    response = await call_next(request)

    # Время окончания обработки запроса
    process_time = time.time() - start_time
    print(f"Обработка запроса заняла: {process_time:.4f} секунд")

    # Логируем статус ответа
    print(f"Статус ответа: {response.status_code}")

    return response

