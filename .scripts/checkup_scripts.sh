# Run formatter
uv run ruff format .

# Check linting rules
uv run ruff check .

# Check mypy
uv run mypy --ignore-missing-imports .
