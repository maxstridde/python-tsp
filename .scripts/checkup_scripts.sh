# Run formatter
uv run ruff format .

# Check linting rules
uv run ruff check . --select=E9,F63,F7,F82 --ignore=E203,W503
# exit-zero treats all errors as warnings
uv run ruff check . --exit-zero --max-complexity=10

# Check mypy
uv run mypy --ignore-missing-imports .
