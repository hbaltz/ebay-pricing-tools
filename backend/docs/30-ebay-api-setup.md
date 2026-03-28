# eBay API Setup

## Overview

The backend uses the **eBay Finding API** (`findCompletedItems` operation) to retrieve
sold listings. This API requires an eBay Developer **App ID** (also called Client ID).

The Finding API is free and does not require user OAuth — only an App ID in the request header.

---

## 1. Create an eBay Developer account

1. Go to [developer.ebay.com](https://developer.ebay.com) and sign in with your eBay account.
2. Navigate to **My Account → Application Keys**.
3. Create a new keyset (or use an existing one).
4. Copy the **App ID (Client ID)** — there are two sets:
   - **Sandbox**: for development and testing against synthetic eBay data
   - **Production**: for live eBay data

---

## 2. Configure environment variables

Copy `.env.example` to `.env` in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```dotenv
EBAY_APP_ID=your-app-id-here
EBAY_ENVIRONMENT=sandbox
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EBAY_APP_ID` | Yes | — | Your eBay Developer App ID (Client ID) |
| `EBAY_ENVIRONMENT` | No | `sandbox` | `sandbox` or `production` |

> **Never commit `.env` to version control.** It is listed in `.gitignore`.

---

## 3. Sandbox vs. Production

| | Sandbox | Production |
|-|---------|------------|
| Data | Synthetic test data | Real eBay listings |
| App ID | Sandbox Client ID | Production Client ID |
| Use when | Developing and testing | Ready for real results |

Start with `EBAY_ENVIRONMENT=sandbox` during development. Switch to `production` only
when you need real pricing data.

---

## 4. API endpoint

```
GET /sold-listings
```

| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `query` | string | Yes | — | 1–200 chars | Search keywords |
| `days` | integer | No | `30` | 1–90 | Number of past days to look back |
| `max_results` | integer | No | `50` | 1–100 | Maximum listings returned |

### Example response

```json
{
  "query": "iPhone 14 Pro 256GB",
  "days": 30,
  "total_results": 12,
  "average_price": 649.99,
  "min_price": 580.00,
  "max_price": 720.00,
  "listings": [
    {
      "item_id": "123456789",
      "title": "Apple iPhone 14 Pro 256GB Space Black Unlocked",
      "sold_price": { "value": 649.99, "currency": "USD" },
      "end_time": "2026-03-25T14:32:00+00:00",
      "condition": "Used",
      "url": "https://www.ebay.com/itm/123456789",
      "image_url": "https://i.ebayimg.com/thumbs/images/...",
      "location": "New York, NY",
      "country": "US"
    }
  ]
}
```

---

## 5. Testing requests from the IDE

See [20-api-test.md](20-api-test.md). Pre-written requests are available in
`backend/http/sold_listings.http`.

---

## 6. eBay Finding API limits

| Limit | Value |
|-------|-------|
| Max results per call | 100 |
| Max lookback window | 90 days |
| Daily call limit (free tier) | 5 000 calls/day |

For heavier usage, monitor your quota in the eBay Developer portal under
**My Account → Usage Reports**.
