from fastapi import FastAPI
from .api.todo_router import todo_router
from .database import init_db_and_tables
from .logging_config import setup_logging
import asyncio


# Set up logging
setup_logging()

app = FastAPI(title="Todo Backend API", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await init_db_and_tables()


# Include routers
app.include_router(todo_router, prefix="/api", tags=["todos"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Backend API"}