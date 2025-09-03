# Justfile

# Create virtual environment
venv:
    python3 -m venv .venv

# Install dependencies
install:
    pip install -r requirements.txt

# Run the development server
dev:
    uvicorn src.app:app --reload

# Run tests
test:
    python3 -m unittest discover tests

# Lint the project
lint:
    ruff check . --fix

# Format the project
format:
    ruff format .

# Default command
default:
    just --list
