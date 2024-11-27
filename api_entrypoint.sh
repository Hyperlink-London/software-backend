#! /usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:/app"

# Run the create_tables.py script at the start of the container
python examples/create_tables.py

# Start the API server
uvicorn src.api_main:app --reload --host 0.0.0.0 --port 8000
