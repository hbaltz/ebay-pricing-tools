# Contributing

## Setup

Install pre-commit hooks once after cloning (from the repo root):

```bash
uv run pre-commit install
```

This registers both the `pre-commit` and `commit-msg` hook stages.

## Commit messages — Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

Format:

```
<type>(<scope>): <short description>
```

`scope` is optional.

### Allowed types

| Type | When to use |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes only |
| `style` | Formatting, whitespace — no logic change |
| `refactor` | Code change that is neither a fix nor a feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD configuration changes |
| `chore` | Maintenance tasks (tooling, config, etc.) |
| `revert` | Reverts a previous commit |

### Examples

```
feat(backend): add listing search endpoint
fix(backend): handle missing price field in eBay response
docs: update ADR for frontend stack choice
chore: upgrade ruff to v0.9.10
```

The `commit-msg` hook will reject any message that does not match this format.

## Code quality — Backend

Python files under `backend/` are linted and formatted automatically by the `pre-commit` hook on every commit (ruff lint + ruff format).

To run manually:

```bash
uv run pre-commit run --all-files
```

See [backend/docs/10-dev-coding-rules.md](backend/docs/10-dev-coding-rules.md) for the full coding standards.
