# Run autopep8 to fix code
uv run black .

# Check other requirements of PEP8
uv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --ignore=E203,W503
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
uv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=79 --statistics

# Check mypy
uv run mypy --ignore-missing-imports .
