from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from .config.settings import settings


# Create the async engine
engine: AsyncEngine = create_async_engine(
    settings.database_url
)