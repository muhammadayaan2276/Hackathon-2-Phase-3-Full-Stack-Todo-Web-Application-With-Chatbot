from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from .config.settings import settings
import re


# Clean the database URL for asyncpg compatibility
database_url = settings.database_url
if 'sslmode=' in database_url or 'channel_binding=' in database_url:
    # Remove problematic parameters for asyncpg compatibility
    database_url = re.sub(r'[&?]sslmode=[^&]*', '', database_url)
    database_url = re.sub(r'[&?]channel_binding=[^&]*', '', database_url)
    # Ensure proper URL format after removals
    database_url = database_url.replace('?&', '?')
    database_url = database_url.rstrip('?&')  # Remove trailing ? or &

# Create the async engine
engine = create_async_engine(
    database_url,
    echo=True,  # Set to True for SQL query logging
)


async def init_db_and_tables():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session