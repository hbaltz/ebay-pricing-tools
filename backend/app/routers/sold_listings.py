"""Router for sold listings endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import Settings, get_settings
from app.schemas.listing import SoldListingsResponse
from app.services.ebay import EbayAPIError, EbayFindingClient

router = APIRouter(prefix="/sold-listings", tags=["sold listings"])


@router.get("", response_model=SoldListingsResponse)
async def get_sold_listings(
    query: Annotated[
        str, Query(min_length=1, max_length=200, description="Search keywords")
    ],
    days: Annotated[
        int, Query(ge=1, le=90, description="Number of past days to search")
    ] = 30,
    max_results: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of results")
    ] = 50,
    settings: Annotated[Settings, Depends(get_settings)] = None,
) -> SoldListingsResponse:
    """Retrieve recently sold eBay listings matching a search query.

    Args:
        query: Search keywords (e.g. "iPhone 14 Pro 256GB").
        days: Number of past days to look back (1–90). Defaults to 30.
        max_results: Maximum number of listings to return (1–100). Defaults to 50.
        settings: Injected application settings.

    Returns:
        Sold listings with aggregated price statistics.

    Raises:
        HTTPException: 502 if the eBay API call fails.
    """
    client = EbayFindingClient(settings)
    try:
        return await client.find_sold_items(
            query=query, days=days, max_results=max_results
        )
    except EbayAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
