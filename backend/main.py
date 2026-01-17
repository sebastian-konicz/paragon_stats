"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize database on startup."""
    init_db()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Analiza paragonow Biedronka w stylu Spotify Wrapped",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS - allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        f"http://localhost:{settings.streamlit_port}",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": "0.1.0",
    }
