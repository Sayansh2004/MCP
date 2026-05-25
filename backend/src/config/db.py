from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,asyncsessionmaker
import os

DB_URL=os.getenv("DATABASE_URL")

engine = create_async_engine(
    DB_URL,
    echo=True
)

AsyncSessionLocal = asyncsessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise

class Base(DeclarativeBase):
    pass