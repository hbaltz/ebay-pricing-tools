"""Pydantic schemas for eBay sold listing data."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class Price(BaseModel):
    """A monetary amount with its currency.

    Attributes:
        value: The numeric amount.
        currency: ISO 4217 currency code (e.g. EUR, USD).
    """

    value: float
    currency: str


class SoldListing(BaseModel):
    """A single completed and sold eBay listing.

    Attributes:
        item_id: eBay item identifier.
        title: Listing title as shown on eBay.
        sold_price: Final sale price.
        end_time: UTC datetime when the listing ended.
        condition: Human-readable condition label (e.g. Used, New).
        url: Direct URL to the eBay listing page.
        image_url: Thumbnail image URL, if available.
        location: Seller-declared item location.
        country: ISO 3166-1 alpha-2 country code of the seller.
    """

    item_id: str
    title: str
    sold_price: Price
    end_time: datetime
    condition: str | None = None
    url: str
    image_url: str | None = None
    location: str | None = None
    country: str | None = None


class SoldListingsResponse(BaseModel):
    """Aggregated response for a sold listings query.

    Attributes:
        query: The search term used.
        days: Number of past days the query covered.
        total_results: Total number of sold listings returned.
        listings: Individual sold listing records.
        average_price: Mean sale price across all results.
        min_price: Lowest sale price among the results.
        max_price: Highest sale price among the results.
    """

    query: str
    days: int
    total_results: int = Field(ge=0)
    listings: list[SoldListing]
    average_price: float | None = None
    min_price: float | None = None
    max_price: float | None = None
