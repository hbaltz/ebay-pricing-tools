# Backend — eBay Pricing Tools API

FastAPI backend for the eBay pricing tools application.

## Tech stack

| Tool | Role |
|------|------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [uvicorn](https://www.uvicorn.org/) | ASGI server |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation & serialisation |
| [httpx](https://www.python-httpx.org/) | Async HTTP client (eBay API calls) |
| [uv](https://docs.astral.sh/uv/) | Python package & project manager |
| [Ruff](https://docs.astral.sh/ruff/) | Linter & formatter |
| [pytest](https://pytest.org/) | Test framework |

## Prerequisites

Install `uv` (if not already present):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Getting started

```bash
# Install dependencies and create virtual environment
uv sync --extra dev

# Install pre-commit hooks (run once, from the repo root)
uv run pre-commit install

# Configure environment variables
cp .env.example .env
# Edit .env and set EBAY_APP_ID (see docs/30-ebay-api-setup.md)

# Run the development server
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

## Project structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app instance & entry point
│   ├── config.py            # Pydantic-settings configuration
│   ├── routers/
│   │   └── sold_listings.py # GET /sold-listings
│   ├── schemas/
│   │   └── listing.py       # SoldListing, SoldListingsResponse
│   └── services/
│       └── ebay.py          # eBay Finding API client
├── tests/                   # pytest test suite
├── http/
│   ├── meta.http            # Health check
│   └── sold_listings.http   # Sold listings queries
├── docs/
│   ├── 10-dev-coding-rules.md  # Linting & style rules
│   ├── 20-api-test.md          # How to run HTTP requests from the IDE
│   └── 30-ebay-api-setup.md    # eBay API credentials & configuration
├── .env.example             # Environment variable template
└── pyproject.toml           # Project metadata & tool config
```

## Development

```bash
uv run ruff check .          # lint
uv run ruff check . --fix    # lint with auto-fix
uv run ruff format .         # format
uv run pytest                # run tests
```

Pre-commit hooks run ruff lint + format automatically on every `git commit` for Python files under `backend/`. To run them manually against all files:

```bash
# from repo root
uv run pre-commit run --all-files
```

## Documentation

| Document | Description |
|----------|-------------|
| [docs/10-dev-coding-rules.md](docs/10-dev-coding-rules.md) | Linting, type annotation & docstring standards |
| [docs/20-api-test.md](docs/20-api-test.md) | How to run HTTP requests from VSCode / JetBrains |
| [docs/30-ebay-api-setup.md](docs/30-ebay-api-setup.md) | eBay Developer account, App ID setup, API limits |

## Architecture decisions

See the project-level [ADR index](../docs/adr/README.md).
