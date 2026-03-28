"""eBay Finding API client.

Wraps the eBay Finding API `findCompletedItems` operation to retrieve
sold listings for a given search query over a configurable time window.

eBay Finding API reference:
https://developer.ebay.com/devzone/finding/callref/findCompletedItems.html
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx

from app.config import Settings
from app.schemas.listing import Price, SoldListing, SoldListingsResponse

_FINDING_API_URLS: dict[str, str] = {
    "production": "https://svcs.ebay.com/services/search/FindingService/v1",
    "sandbox": "https://svcs.sandbox.ebay.com/services/search/FindingService/v1",
}

_MAX_RESULTS_PER_PAGE = 100


class EbayAPIError(Exception):
    """Raised when the eBay Finding API returns an error response.

    Attributes:
        message: Human-readable error description from the API.
        status_code: HTTP status code of the response.
    """

    def __init__(self, message: str, status_code: int = 0) -> None:
        """Initialise the error with a message and optional HTTP status code.

        Args:
            message: Human-readable description of the error.
            status_code: HTTP status code returned by eBay (default 0 if unavailable).
        """
        super().__init__(message)
        self.status_code = status_code


class EbayFindingClient:
    """Async client for the eBay Finding API.

    Attributes:
        settings: Application settings containing the eBay credentials.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialise the client with application settings.

        Args:
            settings: Loaded application settings.
        """
        self._settings = settings
        self._base_url = _FINDING_API_URLS[settings.ebay_environment]

    async def find_sold_items(
        self,
        query: str,
        days: int = 30,
        max_results: int = 50,
    ) -> SoldListingsResponse:
        """Retrieve completed and sold eBay listings matching a search query.

        Args:
            query: Search keywords (e.g. "iPhone 14 Pro 256GB").
            days: Number of past days to search within (1–90). Defaults to 30.
            max_results: Maximum number of listings to return (1–100). Defaults to 50.

        Returns:
            A SoldListingsResponse with the matching listings and aggregated price
            statistics.

        Raises:
            EbayAPIError: If the eBay API returns a failure acknowledgement or an
                HTTP error status.
            ValueError: If `days` or `max_results` are outside their allowed ranges.
        """
        if not 1 <= days <= 90:
            raise ValueError(f"days must be between 1 and 90, got {days}")
        if not 1 <= max_results <= _MAX_RESULTS_PER_PAGE:
            raise ValueError(
                f"max_results must be between 1 and {_MAX_RESULTS_PER_PAGE},"
                f" got {max_results}"
            )

        end_time_from = (datetime.now(UTC) - timedelta(days=days)).strftime(
            "%Y-%m-%dT%H:%M:%S.000Z"
        )

        params = {
            "OPERATION-NAME": "findCompletedItems",
            "SECURITY-APPNAME": self._settings.ebay_app_id,
            "RESPONSE-DATA-FORMAT": "JSON",
            "keywords": query,
            "itemFilter(0).name": "SoldItemsOnly",
            "itemFilter(0).value": "true",
            "itemFilter(1).name": "EndTimeFrom",
            "itemFilter(1).value": end_time_from,
            "paginationInput.entriesPerPage": str(max_results),
            "sortOrder": "EndTimeSoonest",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self._base_url, params=params)

        if response.status_code != 200:
            raise EbayAPIError(
                f"eBay API returned HTTP {response.status_code}",
                status_code=response.status_code,
            )

        data = response.json()
        return self._parse_response(data, query=query, days=days)

    def _parse_response(
        self,
        data: dict,
        query: str,
        days: int,
    ) -> SoldListingsResponse:
        """Parse a raw eBay Finding API JSON response into a SoldListingsResponse.

        Args:
            data: Raw JSON response body from the eBay Finding API.
            query: Original search query string.
            days: Number of past days the query covered.

        Returns:
            A structured SoldListingsResponse.

        Raises:
            EbayAPIError: If the API acknowledgement is not 'Success' or 'Warning'.
        """
        root = data.get("findCompletedItemsResponse", [{}])[0]

        ack = root.get("ack", ["Failure"])[0]
        if ack not in {"Success", "Warning"}:
            error_msg = (
                root.get("errorMessage", [{}])[0]
                .get("error", [{}])[0]
                .get("message", ["Unknown eBay API error"])[0]
            )
            raise EbayAPIError(error_msg)

        raw_items: list[dict] = root.get("searchResult", [{}])[0].get("item", [])

        listings = [self._parse_item(item) for item in raw_items]
        prices = [listing.sold_price.value for listing in listings]

        return SoldListingsResponse(
            query=query,
            days=days,
            total_results=len(listings),
            listings=listings,
            average_price=round(sum(prices) / len(prices), 2) if prices else None,
            min_price=min(prices) if prices else None,
            max_price=max(prices) if prices else None,
        )

    def _parse_item(self, item: dict) -> SoldListing:
        """Parse a single eBay item dict into a SoldListing.

        Args:
            item: Raw item object from the eBay Finding API response.

        Returns:
            A SoldListing populated from the raw item data.
        """
        selling_status = item.get("sellingStatus", [{}])[0]
        raw_price = selling_status.get("currentPrice", [{}])[0]

        listing_info = item.get("listingInfo", [{}])[0]
        condition = item.get("condition", [{}])[0]

        return SoldListing(
            item_id=item.get("itemId", [""])[0],
            title=item.get("title", [""])[0],
            sold_price=Price(
                value=float(raw_price.get("__value__", 0)),
                currency=raw_price.get("@currencyId", "USD"),
            ),
            end_time=datetime.fromisoformat(
                listing_info.get("endTime", ["1970-01-01T00:00:00.000Z"])[0].replace(
                    "Z", "+00:00"
                )
            ),
            condition=condition.get("conditionDisplayName", [None])[0],
            url=item.get("viewItemURL", [""])[0],
            image_url=item.get("galleryURL", [None])[0],
            location=item.get("location", [None])[0],
            country=item.get("country", [None])[0],
        )
