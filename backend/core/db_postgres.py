from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from common.model import Base
from core.config import settings

DATABASE_URL = str(settings.database_url)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = create_async_engine(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session