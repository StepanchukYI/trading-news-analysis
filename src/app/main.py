"""Main FastAPI application."""

from fastapi import FastAPI
from structlog import get_logger

from app.api.v1 import router as api_v1_router

logger = get_logger(__name__)

app = FastAPI(
    title="Trading News Analysis API",
    description="News sentiment analysis for crypto trading signals",
    version="0.1.0",
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup() -> None:
    """Startup initialization."""
    logger.info("Starting Trading News Analysis service")
