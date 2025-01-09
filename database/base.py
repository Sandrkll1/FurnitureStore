import logging
from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

from config import DATABASE_URI

logger = logging.getLogger(__name__)


Base = declarative_base()

engine = create_async_engine(DATABASE_URI, pool_size=20, max_overflow=10, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
language_context = ContextVar('language_code', default='en')


@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def print_model(self):
    text = ", ".join([f"{k}='{v}'" for k, v in self.__dict__.items()][1:])
    return f"<{self.__class__.__name__}({text})>"


def to_dict(self):
    return dict(list(self.__dict__.items())[1:])


Base.__repr__ = print_model
Base.to_dict = to_dict


async def create_tables():
    logger.info("Creating tables...")
    async with engine.begin() as conn:
        for table in Base.metadata.sorted_tables:
            query = text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table.name}')")
            result = await conn.execute(query)
            exists = result.scalar()
            if not exists:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("Tables created.")
                return True
        logger.info("Tables already exist. Skipping creation.")
        return False


async def create_default_roles():
    from .models.user import Role  # Import here to avoid circular imports
    from .models.user import RoleEnum
    logger.info("Creating default roles")
    async with get_session() as session:
        for role in RoleEnum:
            try:
                new_role = Role(name=role.value)
                session.add(new_role)
                logger.info(f"Created role: {role.value}")
            except IntegrityError:
                logger.info(f"Role {role.value} already exists")


async def initialize_database():
    logger.info("Initializing database")
    tables_created = await create_tables()
    if tables_created:
        await create_default_roles()
    else:
        logger.info("Database already initialized. Skipping role creation.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(initialize_database())
