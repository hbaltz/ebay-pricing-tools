# Backend Coding Rules

## Tooling

All rules are enforced by **[Ruff](https://docs.astral.sh/ruff/)** — linter and formatter in one tool, wired into git via **[pre-commit](https://pre-commit.com/)**.

### Pre-commit (automatic, on every `git commit`)

Hooks are defined in `.pre-commit-config.yaml` at the repo root and apply to all Python files under `backend/`:

1. `ruff` — lints and auto-fixes staged files (`--fix --exit-non-zero-on-fix`)
2. `ruff-format` — formats staged files

Install once after cloning (from the repo root):

```bash
uv run pre-commit install
```

Run manually against all files:

```bash
uv run pre-commit run --all-files
```

### Manual (during development)

```bash
uv run ruff check .        # lint
uv run ruff check . --fix  # lint + auto-fix
uv run ruff format .       # format
```

---

## 1. Type Annotations

**Rule set: `ANN` (flake8-annotations)**

All public functions and methods must carry full type annotations on parameters and return types.

```python
# Bad
def get_price(item_id, currency):
    ...

# Good
def get_price(item_id: str, currency: str = "EUR") -> float:
    ...
```

Enabled rules:

| Rule | Description |
|------|-------------|
| `ANN001` | Missing type annotation on function argument |
| `ANN002` | Missing type annotation on `*args` |
| `ANN003` | Missing type annotation on `**kwargs` |
| `ANN201` | Missing return type annotation on public function |
| `ANN202` | Missing return type annotation on private function |
| `ANN204` | Missing return type annotation on special method |

Private helpers (prefixed `_`) are still annotated — `ANN202` is enabled.

Use `from __future__ import annotations` at the top of each file to enable PEP 563 postponed evaluation, allowing forward references and cleaner union syntax (`X | Y` instead of `Union[X, Y]`).

---

## 2. Docstrings — Google Style

**Rule set: `D` (pydocstyle) with `convention = "google"`**

All public modules, classes, and functions must have a docstring in **Google style**.

### Function / method

```python
def search_listings(query: str, max_results: int = 20) -> list[Listing]:
    """Search eBay listings matching a query string.

    Args:
        query: The search term to send to eBay.
        max_results: Maximum number of results to return.

    Returns:
        A list of Listing objects ordered by relevance.

    Raises:
        EbayAPIError: If the eBay API returns a non-2xx response.
    """
```

### Class

```python
class PricingService:
    """Service responsible for computing suggested prices.

    Aggregates sold listing data from eBay and applies
    statistical analysis to produce a pricing recommendation.

    Attributes:
        ebay_client: Async HTTP client for eBay API calls.
        currency: ISO 4217 currency code used for all prices.
    """
```

### Module

```python
"""eBay listing search router.

Exposes endpoints for querying and filtering eBay listings
via the FastAPI router.
"""
```

Enabled rules:

| Rule | Description |
|------|-------------|
| `D100` | Missing docstring in public module |
| `D101` | Missing docstring in public class |
| `D102` | Missing docstring in public method |
| `D103` | Missing docstring in public function |
| `D200` | No whitespaces allowed surrounding docstring text (one-liner) |
| `D205` | 1 blank line required between summary line and description |
| `D213` | Multi-line docstring summary should start at the second line (disabled — Google style uses first line) |
| `D400` | First line should end with a period |
| `D401` | First line should be in imperative mood |
| `D415` | First line should end with period, question mark, or exclamation point |
| `D417` | Missing argument descriptions in the docstring |

`D213` is **disabled** — Google convention places the summary on the first line, not the second.

---

## 3. General Lint Rules

| Rule set | Description |
|----------|-------------|
| `E`, `F` | pycodestyle + pyflakes (baseline correctness) |
| `I` | isort-compatible import ordering |
| `UP` | pyupgrade — enforce modern Python 3.14 syntax |
| `ANN` | Type annotations (see section 1) |
| `D` | Docstrings (see section 2) |

---

## 4. Formatting

Ruff format (replaces Black) is the single source of truth for code style:
- Line length: **88**
- Double quotes for strings
- Trailing commas where valid

Do not configure editors to use other formatters on this project.
