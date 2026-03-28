"""Application entry point.

Creates and configures the FastAPI instance.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.routers import sold_listings

app = FastAPI(
    title="eBay Pricing Tools API",
    description="Backend API for the eBay pricing tools application.",
    version="0.1.0",
)

app.include_router(sold_listings.router)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Check that the API is running.

    Returns:
        A JSON object with a status field set to "ok".
    """
    return {"status": "ok"}
