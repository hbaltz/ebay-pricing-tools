# ADR 001 — Python Backend Framework: FastAPI

## Status

Accepted

## Context

The ebay-pricing-tools backend needs to:

- Query eBay listings data (via eBay API or scraping)
- Process and aggregate pricing information
- Expose a REST API consumed by a frontend application
- Potentially run scheduled or on-demand pricing jobs

Several Python frameworks were considered:

| Framework | Style | Async | Auto docs | Typing |
|-----------|-------|-------|-----------|--------|
| **FastAPI** | Micro/async | Native | Yes (OpenAPI) | Pydantic |
| Flask | Micro/sync | Extensions needed | No | Optional |
| Django + DRF | Full-stack | Partial | Limited | Optional |
| Litestar | Micro/async | Native | Yes (OpenAPI) | Pydantic |

## Decision

**FastAPI** is chosen as the Python backend framework.

### Rationale

1. **Async-first**: eBay data retrieval involves I/O-bound operations (HTTP requests to eBay API, scraping). FastAPI's native `async/await` support makes concurrent requests efficient without threading complexity.

2. **Automatic OpenAPI documentation**: FastAPI generates interactive Swagger UI and ReDoc out of the box. This is valuable for developing and testing endpoints before the frontend is ready, and for future third-party integrations.

3. **Pydantic models**: Data validation and serialization via Pydantic v2 ensures pricing data is well-typed and validated at the boundary. This reduces bugs when handling variable eBay API responses.

4. **Lightweight**: Unlike Django, FastAPI imposes no ORM, admin, or template engine overhead. The tool does not need a full-stack framework.

5. **Ecosystem fit**: Works well with `httpx` (async HTTP for eBay calls), `aiohttp`, and modern Python tooling (`uv`, `ruff`, `pyproject.toml`).

6. **Performance**: One of the fastest Python frameworks (comparable to NodeJS), which matters if the tool is later exposed as a public or shared service.

### Alternatives rejected

- **Flask**: Synchronous by default; async support is bolted on and less ergonomic. No built-in validation or auto-docs.
- **Django + DRF**: Over-engineered for this use case; brings ORM, migrations, admin, and template engine that are not needed.
- **Litestar**: Strong alternative technically, but smaller community and ecosystem than FastAPI. FastAPI's wider adoption means more eBay-related examples and community resources.

## Consequences

- The backend will be structured as a FastAPI application with Pydantic schemas.
- eBay API calls will use `httpx` in async mode.
- The API will self-document at `/docs` (Swagger) and `/redoc`.
- Python version: 3.11+ (required for modern `asyncio` features and Pydantic v2 performance).
- Dependency management: `uv` + `pyproject.toml`.
